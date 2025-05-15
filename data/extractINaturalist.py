import requests
import time

def get_species_from_inaturalist(place_id=141225, taxon_id=None, per_page=200, max_pages=5, delay=1.0):
    base_url = "https://api.inaturalist.org/v1/observations/species_counts"
    all_species = []

    for page in range(1, max_pages + 1):
        params = {
            "place_id": place_id,
            "verifiable": "true",
            "rank": "species",
            "per_page": per_page,
            "page": page
        }
        if taxon_id:
            params["taxon_id"] = taxon_id

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            for item in data.get("results", []):
                taxon = item.get("taxon", {})
                common_name = taxon.get("preferred_common_name", None)
                scientific_name = taxon.get("name", None)
                taxon_id = taxon.get("id", None)

                if taxon_id and scientific_name:
                    all_species.append({
                        "common_name": common_name,
                        "scientific_name": scientific_name,
                        "taxon_id": taxon_id
                    })

            if not data.get("results"):
                break  # no more data

            time.sleep(delay)  # be respectful to the API
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    print(f"✅ Found species")
    return all_species
