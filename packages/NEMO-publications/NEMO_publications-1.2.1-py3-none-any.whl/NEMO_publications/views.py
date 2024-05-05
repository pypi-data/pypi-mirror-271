import json
from urllib.parse import ParseResult, urlparse

from NEMO.decorators import staff_member_required
from NEMO.models import Project, Tool, User
from NEMO.typing import QuerySetType
from NEMO.utilities import BasicDisplayTable, export_format_datetime, queryset_search_filter, quiet_int
from NEMO.views.pagination import SortedPaginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from NEMO_publications.forms import (
    PublicationDataForm,
    create_publication_data_post_form,
    create_publication_metadata_post_form,
)
from NEMO_publications.models import PublicationData, PublicationMetadata, PublicationMetadataStatus
from NEMO_publications.utils import (
    fetch_publication_metadata_by_doi,
)


@login_required
@require_GET
def user_search(request):
    return queryset_search_filter(User.objects.all(), ["first_name", "last_name", "username"], request)


@staff_member_required
@require_POST
def set_publication_status(request, publication_metadata_id):
    publication_metadata = get_object_or_404(PublicationMetadata, id=publication_metadata_id)
    decision_option = [state for state in ["approve", "reject"] if state in request.POST]
    decision = decision_option[0] if len(decision_option) == 1 else None
    if publication_metadata.status:
        return HttpResponseBadRequest("Publication metadata status is already set")
    if decision and not publication_metadata.status:
        if decision == "approve":
            publication_metadata.status = PublicationMetadataStatus.APPROVED
        elif decision == "reject":
            publication_metadata.status = PublicationMetadataStatus.REJECTED
        publication_metadata.decision_time = timezone.now()
        publication_metadata.save()
    return redirect("publications")


@login_required
@require_http_methods(["GET", "POST"])
def create_or_update_publication_data(request, publication_data_id=None, publication_metadata_id=None):
    user: User = request.user
    dictionary = {}

    # Initialize publication data (found: edit, not found: create) and publication metadata (mandatory)
    try:
        publication_data = PublicationData.objects.get(id=publication_data_id)
        publication_metadata = PublicationMetadata.objects.get(id=publication_data.metadata.id)
    except PublicationData.DoesNotExist:
        publication_data = PublicationData()
        # Initialize publication metadata from POST["metadata_id"] - when creating a new publication data entry
        if publication_metadata_id:
            publication_metadata = PublicationMetadata.objects.get(id=publication_metadata_id)
        else:
            return HttpResponseBadRequest("Publication metadata not found.")
    except PublicationMetadata.DoesNotExist:
        return HttpResponseBadRequest("Publication metadata is invalid.")

    if publication_metadata.status == PublicationMetadataStatus.REJECTED:
        return HttpResponseBadRequest("You cannot edit this publication.")

    if request.method == "POST":
        edit = bool(publication_data.id)
        # Only creator can edit publication_data
        if edit and publication_data.creator != user:
            return HttpResponseNotFound("Publication data not found.")
        form = create_publication_data_post_form(request, user, edit, publication_data)
        # Initialize creator and metadata - when creating a new publication data entry
        if not edit:
            form.instance.creator = user
            form.instance.metadata = publication_metadata

        if form.is_valid():
            form.save()
            return redirect("publications")
        else:
            dictionary["form"] = form
            return edit_publication_data(
                request, publication_metadata, dictionary, user, [publication_data.id] if edit else None
            )
    else:
        form = PublicationDataForm(instance=publication_data)
        dictionary["form"] = form
        return edit_publication_data(
            request, publication_metadata, dictionary, user, [publication_data.id] if publication_data.id else None
        )


@login_required
@require_POST
def create_publication_metadata(request):
    user: User = request.user
    metadata_form = create_publication_metadata_post_form(request.POST, user, PublicationMetadata())
    # Can only create publication metadata once, prevent if DOI already exists
    doi = request.POST.get("doi")
    if doi and PublicationMetadata.objects.filter(doi__iexact=doi).exists():
        metadata_form.add_error(None, ["Publication metadata already exists."])
    metadata_form.instance.creator = user
    metadata_form.instance.bibtex = None
    if metadata_form.is_valid():
        publication_metadata = metadata_form.save()
        # Proceed to show publication data form once metadata saved
        return edit_publication_data(
            request,
            publication_metadata,
            {},
            user,
        )
    else:
        return render(request, "NEMO_publications/publication_metadata.html", {"form": metadata_form})


@login_required
@require_http_methods(["GET", "POST"])
def search_publication_by_doi(request):
    user: User = request.user
    if request.method == "POST":
        # DOI is required for search
        doi = request.POST.get("doi")
        if not doi:
            return render(request, "NEMO_publications/publication_search.html", {"error": "DOI is missing"})
        # Remove scheme from doi URL if provided, so we only keep the actual DOI
        parsed_url = urlparse(doi)
        doi = parsed_url.geturl().replace("%s://doi.org/" % parsed_url.scheme, "", 1)
        try:
            # Lookup publication metadata first in database using DOI
            publication_metadata = PublicationMetadata.objects.get(doi__iexact=doi)
            # Do not allow to add rejected publication
            if publication_metadata.status == PublicationMetadataStatus.REJECTED:
                return render(
                    request,
                    "NEMO_publications/publication_search.html",
                    {"error": "You cannot add this publication."},
                )
            try:
                # If user already have a publication data entry for DOI, redirect to publication data edit
                existing_publication_data = PublicationData.objects.get(
                    metadata__id=publication_metadata.id, creator=user
                )
                return redirect("edit_publication", existing_publication_data.id)
            except PublicationData.DoesNotExist:
                return edit_publication_data(
                    request,
                    publication_metadata,
                    {"form": PublicationDataForm(instance=PublicationData())},
                    user,
                )
        except PublicationMetadata.DoesNotExist:
            # If metadata for DOI does not exist in DB, fetch from remote
            publication_metadata_form = fetch_publication_metadata_as_form(doi, user)
            # If metadata was not found remotely or contains errors, display metadata edit form
            if not publication_metadata_form.is_valid():
                return render(
                    request, "NEMO_publications/publication_metadata.html", {"form": publication_metadata_form}
                )
            else:
                publication_metadata = publication_metadata_form.save()
            # When metadata was found or fetched and saved, display publication data entry creation form
            return edit_publication_data(
                request,
                publication_metadata,
                {"form": PublicationDataForm(instance=PublicationData())},
                user,
            )
    else:
        return render(request, "NEMO_publications/publication_search.html")


def fetch_publication_metadata_as_form(doi, user):
    publication_metadata_search = fetch_publication_metadata_by_doi(doi)
    publication_metadata_form = create_publication_metadata_post_form(
        publication_metadata_search["metadata"], user, PublicationMetadata()
    )
    publication_metadata_form.instance.creator = user
    if "error" in publication_metadata_search.keys():
        publication_metadata_form.add_error(None, [publication_metadata_search["error"]])
    return publication_metadata_form


@login_required
@require_GET
def get_publication_leaderboard(request, year=None):
    current_year = timezone.now().year
    selected_year = quiet_int(year, current_year)
    authors_publication_count = User.objects.annotate(
        publication_count=Count(
            "publicationdata__metadata",
            filter=Q(publicationdata__metadata__year=selected_year)
            & ~Q(publicationdata__metadata__status=PublicationMetadataStatus.REJECTED),
        )
    ).filter(publication_count__gt=0)

    page = SortedPaginator(authors_publication_count, request, order_by="-publication_count").get_current_page()
    years = list(PublicationData.objects.values_list("metadata__year", flat=True).distinct())

    if current_year not in years:
        years.insert(0, current_year)
    years.sort(reverse=True)

    return render(
        request,
        "NEMO_publications/leaderboard.html",
        {"page": page, "selected_year": selected_year, "years": years},
    )


@login_required
@require_GET
def get_publications(request):
    user: User = request.user
    # Get all publications that have data entries
    publications_with_data = PublicationMetadata.objects.exclude(publicationdata=None).exclude(
        status=PublicationMetadataStatus.REJECTED
    )
    page = SortedPaginator(publications_with_data, request, order_by="-creation_time").get_current_page()

    if bool(request.GET.get("csv", False)) and user.is_any_part_of_staff:
        return export_publications(publications_with_data.order_by("-creation_time"))

    # Create dictionary associating each publication metadata id with the user's data entry
    user_publication_data = PublicationData.objects.filter(creator=user, metadata__in=page)
    user_publication_data_dict = {}
    for user_publication_data in user_publication_data:
        user_publication_data_dict[user_publication_data.metadata.id] = user_publication_data

    return render(
        request,
        "NEMO_publications/publications.html",
        {"page": page, "user_data": user_publication_data_dict},
    )


@login_required
@require_POST
def delete_publication(request, publication_data_id):
    user = request.user
    # Lookup and delete the user's data entry
    publication = get_object_or_404(PublicationData, pk=publication_data_id)
    if publication.creator != user:
        return HttpResponseBadRequest("You are not allowed to delete this publication data")
    publication.delete()
    return redirect("publications")


def edit_publication_data(request, metadata, dictionary, user, other_users_exclude_data=None):
    dictionary["metadata"] = metadata
    dictionary["projects"] = get_json_project_search_list(user)
    dictionary["tools"] = Tool.objects.all()
    dictionary["authors_suggestion"] = metadata.get_bibtex_authors()
    dictionary["other_users"] = metadata.get_related_data(other_users_exclude_data)
    return render(request, "NEMO_publications/publication_data.html", dictionary)


def get_json_project_search_list(user):
    projects = Project.objects.all()
    if not user.is_any_part_of_staff:
        projects = Project.objects.filter(Q(user=user) | Q(manager_set=user))

    search_list = []
    for project in projects:
        search_list.append(
            {
                "id": project.id,
                "name": project.__str__(),
                "pis": [{"id": pi.id, "name": pi.__str__()} for pi in project.manager_set.all()],
            }
        )
    return mark_safe(json.dumps(search_list))


def export_publications(publication_list: QuerySetType[PublicationMetadata]):
    table = get_publications_table_display(publication_list)
    filename = f"publications_{export_format_datetime()}.csv"
    response = table.to_csv()
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def get_publications_table_display(publication_list: QuerySetType[PublicationMetadata]) -> BasicDisplayTable:
    table = BasicDisplayTable()
    table.add_header(("title", "Title"))
    table.add_header(("journal", "Journal"))
    table.add_header(("year", "Year"))
    table.add_header(("doi", "DOI"))
    table.add_header(("authors", "Authors"))
    table.add_header(("tools", "Tools"))
    table.add_header(("projects", "Projects"))
    table.add_header(("metadata_creators", "Metadata Created By"))
    table.add_header(("data_creators", "Data Created By"))
    table.add_header(("bibtex", "Bibtex"))
    for metadata in publication_list:
        row = {
            "title": metadata.title,
            "journal": metadata.journal,
            "year": metadata.year,
            "doi": metadata.doi,
            "authors": ", ".join([author.__str__() for author in metadata.get_authors()]),
            "tools": ", ".join([tool.__str__() for tool in metadata.get_tools()]),
            "projects": ", ".join([project.__str__() for project in metadata.get_projects()]),
            "metadata_creators": metadata.creator.__str__(),
            "data_creators": ", ".join([project.__str__() for project in metadata.get_data_creators()]),
            "bibtex": metadata.bibtex,
        }
        table.add_row(row)
    return table
