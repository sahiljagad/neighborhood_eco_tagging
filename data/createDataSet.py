import json
import os
from extractEbirdSpecies import get_native_species_from_ebird
from extractINaturalist import get_species_from_inaturalist
from getImages import download_images_for_taxon, get_taxon_id_from_name

FREMONT_PLACE_ID = 141225  # Fremont–Livermore
url = "https://ebird.org/hotspot/L481727/bird-list"

if os.path.exists("species.json"):
        print("species.json found. Loading existing species data.")
        with open("species.json", "r") as f:
            species = json.load(f)
else:
    birds = [get_taxon_id_from_name(bird) for bird in get_native_species_from_ebird(url)]
    native_species = get_species_from_inaturalist(FREMONT_PLACE_ID)
    species = birds + native_species
    filename = "species.json"
    with open(filename, 'w') as file:
        json.dump(species, file, indent=4)

for spec in species:
    print(f"Downloading images for {spec['common_name']}")
    download_images_for_taxon(spec["taxon_id"], spec["common_name"], max_images=50, out_dir="dataset")


