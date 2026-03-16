from PIL import Image
from src.util.path import ASSETS_PATH

def generate_small_facility_icons():
    """
    Processes all 66 raw icons into antialiased assets using the 176x226 logic.
    Filters for 'small' facilities for the current processing run.
    """
    T_WIDTH, T_HEIGHT = 158, 203
    S_WIDTH, S_HEIGHT = 380, 490
    S_Y_OFFSET = 60

    # Complete list of all 66 icons from the game assets
    facilities = [
        # --- Small Slot (Campaign) ---
        {"name": "announcer_booth", "file": "icon_facility_announcer_booth.png", "size": "small"},
        {"name": "bar", "file": "icon_facility_bar.png", "size": "small"},
        {"name": "bedrolls", "file": "icon_facility_bedrolls.png", "size": "small"},
        {"name": "bunkhouse", "file": "icon_facility_bunkhouse.png", "size": "small"},
        {"name": "red_talon_beds", "file": "icon_facility_DLC2_rt_beds.png", "size": "small"},
        {"name": "red_talon_officers_quarters", "file": "icon_facility_DLC2_rt_officers_quarters.png", "size": "small"},
        {"name": "red_talon_watchtower", "file": "icon_facility_DLC2_rt_watchtower.png", "size": "small"},
        {"name": "red_talon_workshop", "file": "icon_facility_DLC2_rt_workshop.png", "size": "small"},
        {"name": "incinerator", "file": "icon_facility_faustite_incinerator.png", "size": "small"},
        {"name": "meditation_garden", "file": "icon_facility_faustite_meditation_garden.png", "size": "small"},
        {"name": "fire_safe_storage", "file": "icon_facility_fire_safe_storage.png", "size": "small"},
        {"name": "fuel_tank", "file": "icon_facility_fuel_tank.png", "size": "small"},
        {"name": "garden", "file": "icon_facility_garden.png", "size": "small"},
        {"name": "gas_generator", "file": "icon_facility_gas_generator.png", "size": "small"},
        {"name": "general_storage", "file": "icon_facility_general_storage.png", "size": "small"},
        {"name": "hydroponics", "file": "icon_facility_hydroponics.png", "size": "small"},
        {"name": "infirmary", "file": "icon_facility_infirmary.png", "size": "small"},
        {"name": "kitchen", "file": "icon_facility_kitchen.png", "size": "small"},
        {"name": "latrine", "file": "icon_facility_latrine.png", "size": "small"},
        {"name": "rain_collector", "file": "icon_facility_rain_collector.png", "size": "small"},
        {"name": "shooting_range", "file": "icon_facility_shooting_platform.png", "size": "small"},
        {"name": "still", "file": "icon_facility_still.png", "size": "small"},
        {"name": "fighting_gym", "file": "icon_facility_training_area.png", "size": "small"},
        {"name": "workshop", "file": "icon_facility_workshop.png", "size": "small"},
        
        # --- Large Slot (Campaign) ---
        {"name": "armory", "file": "icon_facility_armory.png", "size": "large"},
        {"name": "auto_shop", "file": "icon_facility_auto_shop.png", "size": "large"},
        {"name": "barracks", "file": "icon_facility_barracks.png", "size": "large"},
        {"name": "cleo_uplink", "file": "icon_facility_DLC2_cleo_uplink.png", "size": "large"},
        {"name": "farm", "file": "icon_facility_farm.png", "size": "large"},
        {"name": "haven_device", "file": "icon_facility_faustite_haven_device.png", "size": "large"},
        {"name": "forge", "file": "icon_facility_forge.png", "size": "large"},
        {"name": "lounge", "file": "icon_facility_lounge.png", "size": "large"},
        {"name": "solar_array", "file": "icon_facility_solar_array.png", "size": "large"},
        {"name": "staging_area", "file": "icon_facility_staging_area.png", "size": "large"},
        {"name": "trade_depot", "file": "icon_facility_trade_depot.png", "size": "large"},
        {"name": "hospital", "file": "icon_facility_hospital.png", "size": "large"},

        # --- Heartland DLC / Specialty ---
        {"name": "heartland_defenses", "file": "icon_facility_heartland_defenses.png", "size": "large"},
        {"name": "heartland_depot", "file": "icon_facility_heartland_depot.png", "size": "large"},
        {"name": "heartland_vehicles", "file": "icon_facility_heartland_depot_vehicles.png", "size": "small"},
        {"name": "heartland_weapons", "file": "icon_facility_heartland_depot_weapons.png", "size": "small"},
        {"name": "heartland_fabricator", "file": "icon_facility_heartland_fabricator_shop.png", "size": "small"},
        {"name": "heartland_farm", "file": "icon_facility_heartland_farm.png", "size": "large"},
        {"name": "heartland_fuel_extractor", "file": "icon_facility_heartland_fuel_extractor.png", "size": "small"},
        {"name": "heartland_kitchen", "file": "icon_facility_heartland_hunters_kitchen.png", "size": "small"},
        {"name": "heartland_lab", "file": "icon_facility_heartland_lab.png", "size": "small"},
        {"name": "heartland_explosives", "file": "icon_facility_heartland_lab_explosives.png", "size": "small"},
        {"name": "heartland_fire_lab", "file": "icon_facility_heartland_lab_fire.png", "size": "small"},
        {"name": "medical_expansion", "file": "icon_facility_heartland_medical_expansion.png", "size": "small"},
        {"name": "pharmacy_expansion", "file": "icon_facility_heartland_medical_expansion_pharmacy.png", "size": "small"},
        {"name": "plague_expansion", "file": "icon_facility_heartland_medical_expansion_plague_lab.png", "size": "small"},
        {"name": "medical_tent", "file": "icon_facility_heartland_medical_tent.png", "size": "small"},
        {"name": "heartland_radio", "file": "icon_facility_heartland_radio.png", "size": "small"},
        {"name": "heartland_uplink", "file": "icon_facility_heartland_uplink.png", "size": "small"},
        {"name": "heartland_utilities", "file": "icon_facility_heartland_utilities.png", "size": "large"},
        
        # --- Unique / Pre-built ---
        {"name": "junk", "file": "icon_facility_junk.png", "size": "small"},
        {"name": "laboratory", "file": "icon_facility_laboratory.png", "size": "small"},
        {"name": "outdoor_projector", "file": "icon_facility_outdoor_projector.png", "size": "large"},
        {"name": "parking_empty", "file": "icon_facility_parking_empty.png", "size": "small"},
        {"name": "parking_full", "file": "icon_facility_parking_full.png", "size": "small"},
        {"name": "radio_room", "file": "icon_facility_radio_room.png", "size": "small"},
        {"name": "refrigerated_storage", "file": "icon_facility_refrigerated_storage.png", "size": "small"},
        {"name": "scrap_storage", "file": "icon_facility_scrap_storage.png", "size": "small"},
        {"name": "showers", "file": "icon_facility_showers.png", "size": "small"},
        {"name": "sniper_perch", "file": "icon_facility_sniper_perch.png", "size": "small"},
        {"name": "suite", "file": "icon_facility_suite.png", "size": "small"},
        {"name": "target_lineup", "file": "icon_facility_target_lineup.png", "size": "small"},
    ]

    raw_dir = ASSETS_PATH / "synthetic_data" / "icons" / "raw" / "common_facilities"
    output_dir = ASSETS_PATH / "synthetic_data" / "icons" / "facility" / "small"
    output_dir.mkdir(parents=True, exist_ok=True)

    small_facilities = [f for f in facilities if f["size"] == "small"]

    for facility in small_facilities:
        raw_path = raw_dir / facility["file"]
        if not raw_path.exists():
            print(f"Warning: Could not find {raw_path}")
            continue

        with Image.open(raw_path).convert("RGBA") as raw_icon:
            # --- RENDERING ---
            # Using the transparency canvas with your tweaked dimensions
            canvas = Image.new("RGBA", (S_WIDTH, S_HEIGHT), (0, 0, 0, 0))
            
            # Centering logic with your verified +1 X-offset
            off_x = (S_WIDTH - raw_icon.width) // 2
            off_y = S_Y_OFFSET
            
            # Paste raw icon directly to keep original colors/alpha
            canvas.paste(raw_icon, (off_x + 1, off_y), raw_icon)

            # Downscale to 1x target
            final_icon = canvas.resize((T_WIDTH, T_HEIGHT), Image.Resampling.LANCZOS)

            # Save final PNG
            output_path = output_dir / f"{facility['name']}.png"
            final_icon.save(output_path)
            print(f"  - Generated: {facility['name']}.png")

def run():
    print("--- Starting Facility Icon Generation (176x226 -> 158x203) ---")
    generate_small_facility_icons()

if __name__ == "__main__":
    run()