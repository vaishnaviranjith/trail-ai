# -*- coding: utf-8 -*-
"""
Builder script to generate comprehensive 38-district Tamil Nadu dataset:
trail ai/backend/data/tamilnadu_complete_seed.json
"""
import json
import os

def create_complete_dataset():
    data = {
        "destination": "Tamil Nadu",
        "state": "Tamil Nadu",
        "country": "India",
        "currency": "INR",
        "description": "Comprehensive 38-district travel intelligence system for Tamil Nadu. Spanning ancient Dravidian temple gopurams, misty Western Ghat hill sanctuaries, UNESCO Chola monoliths, royal Chettinad culinary merchant estates, vibrant Kongu heartlands, and sacred oceanic capes.",
        "center_coordinates": {
            "lat": 10.7905,
            "lng": 78.7047
        },
        "emergency_contacts": [
            { "name": "Tamil Nadu Tourist Helpline (Toll-Free 24x7)", "phone": "1800-4253-1111", "type": "Tourism" },
            { "name": "State Police Emergency", "phone": "112", "type": "Police" },
            { "name": "State Medical Ambulance", "phone": "108", "type": "Medical" },
            { "name": "State Disaster Management Response", "phone": "1077", "type": "Emergency" },
            { "name": "Nilgiris Mountain Ghat Control Room", "phone": "+91-423-2443977", "type": "Highways" },
            { "name": "Kodaikanal Hill Safety Helpline", "phone": "+91-4542-241379", "type": "Highways" },
            { "name": "Madurai Heritage Information Desk", "phone": "+91-452-2334757", "type": "Tourism" },
            { "name": "Coimbatore Tourism Center", "phone": "+91-422-2303176", "type": "Tourism" },
            { "name": "Kanyakumari Coast Guard & Helpline", "phone": "+91-4652-246261", "type": "Maritime" }
        ],
        "ghat_corridors": [
            {
                "id": "ghat_cbe_nilgiris",
                "from_district": "Coimbatore",
                "to_district": "Nilgiris",
                "corridor_name": "Mettupalayam - Coonoor - Ooty Ghat Road (NH 181)",
                "hairpin_bends": 36,
                "ghat_speed_kmh": 26,
                "buffer_minutes": 25,
                "scenic_note": "Mountain ascent via Mettupalayam-Coonoor pass with 36 hairpin bends and tea estate mist (~26 km/h + 25m mountain safety buffer)."
            },
            {
                "id": "ghat_dgl_kodaikanal",
                "from_district": "Dindigul",
                "to_district": "Dindigul",
                "corridor_name": "Batlagundu - Palani Ghat Road to Kodaikanal (SH 156)",
                "hairpin_bends": 18,
                "ghat_speed_kmh": 28,
                "buffer_minutes": 20,
                "scenic_note": "Ascent through Palani Ghat Road with misty valley overlooks and pine scent (~28 km/h + 20m mountain buffer)."
            },
            {
                "id": "ghat_slm_yercaud",
                "from_district": "Salem",
                "to_district": "Salem",
                "corridor_name": "Salem - Yercaud Ghat Road (SH 188)",
                "hairpin_bends": 20,
                "ghat_speed_kmh": 28,
                "buffer_minutes": 15,
                "scenic_note": "Winding 20-hairpin climb to Shevaroy hills with panoramic views of Salem city basin (~28 km/h)."
            },
            {
                "id": "ghat_nmk_kolli",
                "from_district": "Namakkal",
                "to_district": "Namakkal",
                "corridor_name": "Semmedu - Kolli Hills Ghat Pass",
                "hairpin_bends": 70,
                "ghat_speed_kmh": 24,
                "buffer_minutes": 30,
                "scenic_note": "Thrilling 70-hairpin bend climb through dense forest to the Kolli hill range (~24 km/h + 30m buffer)."
            },
            {
                "id": "ghat_theni_meghamalai",
                "from_district": "Theni",
                "to_district": "Theni",
                "corridor_name": "Chinnamanur - Highwavys Meghamalai Ghat",
                "hairpin_bends": 18,
                "ghat_speed_kmh": 24,
                "buffer_minutes": 25,
                "scenic_note": "Remote mountain ghat through cardamom and tea plantations to Highwavys Cloud Mountain (~24 km/h)."
            },
            {
                "id": "hwy_mdu_ram",
                "from_district": "Madurai",
                "to_district": "Ramanathapuram",
                "corridor_name": "Madurai - Rameswaram Pamban Sea Corridor (NH 87)",
                "hairpin_bends": 0,
                "ghat_speed_kmh": 60,
                "buffer_minutes": 10,
                "scenic_note": "Scenic coastal highway crossing the historic Pamban Sea Bridge to Rameswaram Island (~60 km/h)."
            },
            {
                "id": "hwy_thanj_trichy",
                "from_district": "Thanjavur",
                "to_district": "Tiruchirappalli",
                "corridor_name": "Cauvery Delta Chola Heritage Highway (NH 83)",
                "hairpin_bends": 0,
                "ghat_speed_kmh": 65,
                "buffer_minutes": 10,
                "scenic_note": "Smooth 4-lane highway across fertile Cauvery delta fields connecting UNESCO living Chola monuments (~65 km/h)."
            }
        ],
        "districts": {},
        "pois": [],
        "hotels": [],
        "food_places": []
    }

    # Helper function to append district
    def add_district(dist_id, name, aliases, region, hq, lat, lng, is_ghat, elev, desc, specialties, pois, hotels, foods):
        dist_obj = {
            "district_id": dist_id,
            "name": name,
            "alias_names": aliases,
            "region": region,
            "headquarters": hq,
            "center_coordinates": {"lat": lat, "lng": lng},
            "is_ghat_region": is_ghat,
            "elevation_m": elev,
            "ghat_road_speed_kmh": 26 if is_ghat else 55,
            "highway_speed_kmh": 65,
            "description": desc,
            "food_specialties": specialties,
            "pois": pois,
            "hotels": hotels,
            "food_places": foods
        }
        data["districts"][dist_id] = dist_obj
        data["pois"].extend(pois)
        data["hotels"].extend(hotels)
        data["food_places"].extend(foods)

    # 1. Chennai
    add_district(
        "chennai", "Chennai", ["chennai", "madras"], "Tondai Nadu", "Chennai", 13.0827, 80.2707, False, 15,
        "Tamil Nadu's bustling cultural and coastal capital, celebrated for heritage Dravidian temples, colonial British architecture, Carnatic music sabhas, and vibrant Marina shoreline.",
        ["Filter Kaapi", "Mylapore Ghee Roast Dosa", "Marina Beach Sundal", "Sowcarpet Murukku Sandwich", "Idiyappam with Coconut Milk"],
        [
            {
                "id": "poi_chn_kapaleeshwarar", "name": "Kapaleeshwarar Temple, Mylapore", "district": "Chennai", "category": "Heritage",
                "tags": ["temple", "heritage", "dravidian", "culture", "sculpture"],
                "lat": 13.0334, "lng": 80.2699, "rating": 4.8, "review_count": 42000, "entry_fee_per_person": 0, "typical_duration_minutes": 90,
                "opening_time": "06:00", "closing_time": "21:00",
                "description": "7th-century CE Shaivite temple built in Dravidian style with a 37-meter rainbow gopuram, holy Kapaleeshwarar tank, and peacocks dedicated to Goddess Karpagambal.",
                "best_time_to_visit": "Early Morning / Evening", "difficulty": "Easy"
            },
            {
                "id": "poi_chn_marina_beach", "name": "Marina Beach & Lighthouse, Chennai", "district": "Chennai", "category": "Beaches",
                "tags": ["beach", "lighthouse", "sunset", "promenade", "street_food"],
                "lat": 13.0500, "lng": 80.2824, "rating": 4.5, "review_count": 78000, "entry_fee_per_person": 20, "typical_duration_minutes": 100,
                "opening_time": "05:00", "closing_time": "22:00",
                "description": "One of the longest natural urban beaches in the world (13 km), featuring an elevator-accessible maritime lighthouse overlooking the Bay of Bengal and animated beachside sundal stalls.",
                "best_time_to_visit": "Sunrise / Sunset", "difficulty": "Easy"
            },
            {
                "id": "poi_chn_fort_st_george", "name": "Fort St. George & Clive Museum", "district": "Chennai", "category": "Heritage",
                "tags": ["history", "museum", "colonial", "british", "architecture"],
                "lat": 13.0797, "lng": 80.2874, "rating": 4.4, "review_count": 18000, "entry_fee_per_person": 25, "typical_duration_minutes": 90,
                "opening_time": "09:00", "closing_time": "17:00",
                "description": "First British fortress in India founded in 1644, housing St. Mary's Church and Clive Museum displaying period arms, medals, and silver coins.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_chn_marina_heritage", "name": "Marina Grand Heritage Inn, Chennai", "district": "Chennai", "category": "Budget Hotel",
                "price_per_night": 1700, "rating": 4.4, "review_count": 1450, "lat": 13.0420, "lng": 80.2720,
                "address": "Radhakrishnan Salai, Mylapore, Chennai", "amenities": ["Free Wi-Fi", "Air Conditioning", "South Indian Breakfast", "24/7 Front Desk"],
                "room_type": "Deluxe AC Executive Room", "description": "Comfortable stay located minutes from Mylapore temple and Marina promenade."
            }
        ],
        [
            {
                "id": "food_chn_ratna_cafe", "name": "Ratna Cafe Triplicane Since 1948", "district": "Chennai", "category": "Local Food",
                "cuisine": "Traditional Chennai Vegetarian", "specialties": ["Legendary Bottomless Sambar Idli", "Crispy Masala Vadai", "Ghee Rava Dosa", "Degree Filter Coffee"],
                "cost_for_two": 260, "rating": 4.7, "review_count": 31000, "lat": 13.0560, "lng": 80.2740, "opening_time": "06:30", "closing_time": "22:30",
                "description": "An undisputed Chennai culinary landmark famous for waiters pouring piping hot aromatic sambar from stainless steel jugs over cloud-like idlis."
            }
        ]
    )

    # 2. Chengalpattu
    add_district(
        "chengalpattu", "Chengalpattu", ["chengalpattu", "mahabalipuram", "mamallapuram", "chengalpet"], "Tondai Nadu / Coastal", "Chengalpattu", 12.6841, 79.9836, False, 36,
        "Gateway to the UNESCO World Heritage monuments of Mamallapuram, rocky monolithic cave temples, pristine East Coast Road beaches, and tranquil Vedanthangal wetlands.",
        ["Mahabalipuram Fresh Coastal Fish Fry", "Prawn Masala Roast", "Coconut Water Palm Jaggery Payasam"],
        [
            {
                "id": "poi_cgp_shore_temple", "name": "Shore Temple & Pancha Rathas, Mahabalipuram", "district": "Chengalpattu", "category": "Heritage",
                "tags": ["unesco", "heritage", "monolith", "pallava", "beach"],
                "lat": 12.6167, "lng": 80.1983, "rating": 4.8, "review_count": 65000, "entry_fee_per_person": 40, "typical_duration_minutes": 120,
                "opening_time": "06:00", "closing_time": "18:00",
                "description": "8th-century structural granite temple standing right against the Bay of Bengal surf, alongside monolithic five rathas carved from single boulders by King Narasimhavarman I.",
                "best_time_to_visit": "Early Morning / Golden Hour", "difficulty": "Easy"
            },
            {
                "id": "poi_cgp_vedanthangal", "name": "Vedanthangal Bird Sanctuary", "district": "Chengalpattu", "category": "Wildlife",
                "tags": ["birds", "wildlife", "lake", "nature", "photography"],
                "lat": 12.5458, "lng": 79.8550, "rating": 4.5, "review_count": 21000, "entry_fee_per_person": 25, "typical_duration_minutes": 120,
                "opening_time": "06:00", "closing_time": "18:00",
                "description": "India's oldest water bird sanctuary (est. 1798), hosting over 40,000 migratory waterfowl including painted storks, spoonbills, and grey pelicans nesting on Barringtonia trees.",
                "best_time_to_visit": "Early Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_cgp_sea_breeze", "name": "Mahabalipuram Sea Breeze Resort", "district": "Chengalpattu", "category": "Budget Hotel",
                "price_per_night": 2200, "rating": 4.3, "review_count": 1200, "lat": 12.6200, "lng": 80.1950,
                "address": "Othavadai Street, Mahabalipuram", "amenities": ["Swimming Pool", "Beach Walkway", "Air Conditioning", "Free Breakfast"],
                "room_type": "Coastal Cottage", "description": "Laidback coastal stay offering immediate access to the beach and shore temple views."
            }
        ],
        [
            {
                "id": "food_cgp_moonrakers", "name": "Moonrakers Coastal Kitchen, Mahabalipuram", "district": "Chengalpattu", "category": "Local Food",
                "cuisine": "Fresh Coastal Seafood & South Indian", "specialties": ["Tawa Fried King Fish", "Garlic Butter Prawns", "Crab Masala", "Banana Flower Fritters"],
                "cost_for_two": 580, "rating": 4.6, "review_count": 18000, "lat": 12.6185, "lng": 80.1945, "opening_time": "11:00", "closing_time": "23:00",
                "description": "Legendary traveler favorite serving daily fresh catches seasoned with native Tamil beachside masalas."
            }
        ]
    )

    # 3. Kanchipuram
    add_district(
        "kanchipuram", "Kanchipuram", ["kanchipuram", "kanchi", "conjeevaram"], "Tondai Nadu", "Kanchipuram", 12.8342, 79.7036, False, 88,
        "The golden 'City of Thousand Temples' and sacred silk capital of India, revered for soaring Rajagopurams, ancient Pallava rock architecture, and exquisite handwoven pure mulberry silk sarees.",
        ["Authentic Kanchipuram Kovil Idli (steamed in bauhinia leaves with ginger & pepper)", "Kovil Puliyodharai", "Kanchi Ghee Pongal"],
        [
            {
                "id": "poi_kan_ekambareswarar", "name": "Ekambareswarar Temple (Earth Stalam)", "district": "Kanchipuram", "category": "Heritage",
                "tags": ["temple", "pancha_bhoota", "heritage", "earth", "gopuram"],
                "lat": 12.8475, "lng": 79.7001, "rating": 4.8, "review_count": 31000, "entry_fee_per_person": 0, "typical_duration_minutes": 100,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "One of the five Pancha Bhoota Sthalams representing Earth (Prithvi Lingam), boasting a colossal 59-meter 11-tier gopuram and a sacred 3,500-year-old four-branched mango tree.",
                "best_time_to_visit": "Morning / Evening", "difficulty": "Easy"
            },
            {
                "id": "poi_kan_kailasanathar", "name": "Kailasanathar Temple, Kanchipuram", "district": "Kanchipuram", "category": "Heritage",
                "tags": ["pallava", "sandstone", "ancient", "architecture", "sculpture"],
                "lat": 12.8423, "lng": 79.6900, "rating": 4.7, "review_count": 19500, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "06:00", "closing_time": "18:00",
                "description": "The oldest surviving sandstone temple structure in Kanchipuram built in 700 CE by Pallava King Rajasimha, lined with 58 small shrines displaying delicate stone carvings.",
                "best_time_to_visit": "Early Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_kan_krishna_grand", "name": "Sri Krishna Grand Residency Kanchipuram", "district": "Kanchipuram", "category": "Budget Hotel",
                "price_per_night": 1600, "rating": 4.4, "review_count": 920, "lat": 12.8310, "lng": 79.7080,
                "address": "Gandhi Road, Kanchipuram", "amenities": ["Free Wi-Fi", "Pure Veg Restaurant", "Air Conditioning", "Temple Assistance"],
                "room_type": "Executive Double AC Room", "description": "Modern budget hotel centrally located near silk weaving handloom centers and Ekambareswarar Temple."
            }
        ],
        [
            {
                "id": "food_kan_saravana_bhavan", "name": "Sri Saravana Bhavan Kanchi Temple View", "district": "Kanchipuram", "category": "Local Food",
                "cuisine": "Traditional Kanchi Temple Style", "specialties": ["Signature Kanchipuram Kovil Idli", "Tamarind Puliyodharai", "Ghee Podi Roast", "Mysore Pak"],
                "cost_for_two": 220, "rating": 4.6, "review_count": 14000, "lat": 12.8330, "lng": 79.7040, "opening_time": "06:00", "closing_time": "22:00",
                "description": "Renowned for serving authentic spiced Kanchipuram idlis steamed inside fragrant leaf cups."
            }
        ]
    )

    # 4. Thiruvallur
    add_district(
        "thiruvallur", "Thiruvallur", ["thiruvallur", "tiruvallur"], "Tondai Nadu", "Thiruvallur", 13.1432, 79.9079, False, 38,
        "Famed for the grand Sri Veeraraghava Swamy temple, Poondi reservoir wetlands, and ecological coastal Pulicat lagoon sanctuaries.",
        ["Poondi Fresh Catch Fish Fry", "Thiruvallur Crispy Rava Dosa", "Traditional Buttermilk Sambaram"],
        [
            {
                "id": "poi_tlr_veeraraghava", "name": "Sri Veeraraghava Swamy Temple", "district": "Thiruvallur", "category": "Heritage",
                "tags": ["temple", "divya_desam", "vaishnava", "healing"],
                "lat": 13.1415, "lng": 79.9042, "rating": 4.7, "review_count": 17000, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "Ancient Divya Desam shrine dedicated to Lord Vishnu in reclining posture, famed for Hruthtapanasini holy water tank.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            },
            {
                "id": "poi_tlr_poondi_reservoir", "name": "Poondi Reservoir & Nature Park", "district": "Thiruvallur", "category": "Nature & Plantations",
                "tags": ["reservoir", "nature", "lake", "picnic"],
                "lat": 13.1904, "lng": 79.8601, "rating": 4.3, "review_count": 8900, "entry_fee_per_person": 15, "typical_duration_minutes": 90,
                "opening_time": "09:00", "closing_time": "17:30",
                "description": "Scenic water reservoir (Sathyamurthy Sagar) on the Kosasthalaiyar river surrounded by acacia woodlands and migratory water bird spots.",
                "best_time_to_visit": "Afternoon / Evening", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_tlr_inn", "name": "Golden Park Inn Thiruvallur", "district": "Thiruvallur", "category": "Budget Hotel",
                "price_per_night": 1400, "rating": 4.2, "review_count": 510, "lat": 13.1420, "lng": 79.9060,
                "address": "JN Road, Thiruvallur", "amenities": ["Air Conditioning", "Free Parking", "Veg Restaurant"],
                "room_type": "Standard Deluxe Room", "description": "Clean, hospitable accommodation walking distance to the historic temple and railway transit."
            }
        ],
        [
            {
                "id": "food_tlr_balaji_mess", "name": "Sri Balaji Vegetarian Mess, Thiruvallur", "district": "Thiruvallur", "category": "Local Food",
                "cuisine": "Traditional Tamil Tiffin", "specialties": ["Ghee Pongal with Medu Vada", "Hot Filter Kaapi", "Onion Rava Dosa"],
                "cost_for_two": 200, "rating": 4.5, "review_count": 4800, "lat": 13.1430, "lng": 79.9070, "opening_time": "06:30", "closing_time": "21:30",
                "description": "Beloved local tiffin canteen famous for crispy vadas and traditional banana leaf meals."
            }
        ]
    )

    # 5. Vellore
    add_district(
        "vellore", "Vellore", ["vellore"], "Northern Palar Valley", "Vellore", 12.9165, 79.1325, False, 216,
        "Historic fortress city anchored by the massive 16th-century granite Vellore Fort, Jalakanteswarar temple, and Sripuram golden temple.",
        ["Vellore Brinjal Khatta (Spicy Tangy Baingan Curry)", "Palar Valley Dum Biryani", "Walajah Badam Peda"],
        [
            {
                "id": "poi_vel_fort", "name": "16th-Century Vellore Fort & Jalakanteswarar Temple", "district": "Vellore", "category": "Heritage",
                "tags": ["fort", "moat", "vijayanagara", "heritage", "architecture"],
                "lat": 12.9236, "lng": 79.1325, "rating": 4.7, "review_count": 45000, "entry_fee_per_person": 0, "typical_duration_minutes": 120,
                "opening_time": "08:00", "closing_time": "18:00",
                "description": "Massive granite stone fort surrounded by a wide water moat, enclosing the Vijayanagara-style Jalakanteswarar temple and Tipu Sultan's royal quarters.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            },
            {
                "id": "poi_vel_golden_temple", "name": "Sripuram Golden Temple (Malaikodi)", "district": "Vellore", "category": "Heritage",
                "tags": ["golden_temple", "spiritual", "architecture", "gardens"],
                "lat": 12.8711, "lng": 79.0886, "rating": 4.8, "review_count": 52000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "07:00", "closing_time": "20:00",
                "description": "Spiritual sanctuary covered with over 1,500 kilograms of pure gold foil set within a lush star-shaped green walkway and landscaped water fountains.",
                "best_time_to_visit": "Evening (Illuminated)", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_vel_grand_days", "name": "GRT Grand Days Vellore", "district": "Vellore", "category": "Budget Hotel",
                "price_per_night": 2400, "rating": 4.5, "review_count": 2100, "lat": 12.9260, "lng": 79.1350,
                "address": "Gandhinagar, Vellore", "amenities": ["Swimming Pool", "Fitness Center", "Multi-Cuisine Dining", "Free Wi-Fi"],
                "room_type": "Executive King Room", "description": "Premium comfort hotel positioned close to Vellore Fort and highway connecting Chennai & Bengaluru."
            }
        ],
        [
            {
                "id": "food_vel_saravana", "name": "Hotel Saravana Pure Veg Vellore", "district": "Vellore", "category": "Local Food",
                "cuisine": "South Indian Vegetarian", "specialties": ["Ghee Roast Masala Dosa", "Filter Kaapi", "Mini Tiffin Platter"],
                "cost_for_two": 240, "rating": 4.6, "review_count": 11000, "lat": 12.9180, "lng": 79.1310, "opening_time": "06:30", "closing_time": "22:00",
                "description": "Popular breakfast and dinner destination offering crispy dosas and rich sambar."
            }
        ]
    )

    # 6. Ranipet
    add_district(
        "ranipet", "Ranipet", ["ranipet", "arcot", "walajah"], "Northern Palar", "Ranipet", 12.9272, 79.3330, False, 160,
        "Historic Nawabi heartland encompassing Arcot, famed for the historic Delhi Gate, Walajah sweet heritage, and 7th-century Mahendravadi rock-cut cave shrines.",
        ["Arcot Authentic Mutton Biryani", "Walajah Pure Ghee Badam Halwa", "Spicy Arcot Parotta"],
        [
            {
                "id": "poi_rnp_delhi_gate", "name": "Delhi Gate & Arcot Fort Heritage Enclave", "district": "Ranipet", "category": "Heritage",
                "tags": ["nawab", "history", "monument", "british", "clive"],
                "lat": 12.9064, "lng": 79.3353, "rating": 4.3, "review_count": 4800, "entry_fee_per_person": 0, "typical_duration_minutes": 60,
                "opening_time": "08:00", "closing_time": "18:00",
                "description": "Red-brick gateway standing as the sole remnant of the historic Siege of Arcot (1751) fought by Robert Clive and the Nawab of the Carnatic.",
                "best_time_to_visit": "Morning / Late Afternoon", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_rnp_highway", "name": "Ranipet Highway Residency", "district": "Ranipet", "category": "Budget Hotel",
                "price_per_night": 1500, "rating": 4.2, "review_count": 620, "lat": 12.9290, "lng": 79.3310,
                "address": "Arcot Road, Ranipet", "amenities": ["Air Conditioning", "Free Wi-Fi", "Restaurant"],
                "room_type": "Standard AC Room", "description": "Convenient transit basecamp situated on the Chennai-Bengaluru arterial route."
            }
        ],
        [
            {
                "id": "food_rnp_arcot_biryani", "name": "Star Biryani & Halwa Stall, Arcot", "district": "Ranipet", "category": "Local Food",
                "cuisine": "Carnatic Nawabi Traditional", "specialties": ["Fragrant Arcot Mutton Dum Biryani", "Walajah Ghee Halwa", "Ennai Kathirikai Curry"],
                "cost_for_two": 420, "rating": 4.7, "review_count": 14500, "lat": 12.9050, "lng": 79.3360, "opening_time": "11:30", "closing_time": "22:30",
                "description": "Celebrated since the Nawabi era for aromatic short-grain mutton biryani cooked over wood fires."
            }
        ]
    )

    # 7. Tirupattur
    add_district(
        "tirupattur", "Tirupattur", ["tirupattur", "yelagiri", "ambur", "tirupathur"], "Northern Highlands (Javadi Hills)", "Tirupattur", 12.4950, 78.5678, True, 1110,
        "Highland district featuring the pristine Yelagiri hill station, 14 hairpin bend scenic ghat road, cascading Jalagamparai waterfalls, and world-renowned Ambur biryani culinary culture.",
        ["Ambur Seeraga Samba Dum Biryani", "Yelagiri Wild Honey Pancakes", "Javadi Millet Roti with Nattu Kozhi Curry"],
        [
            {
                "id": "poi_tpt_yelagiri_nature_park", "name": "Yelagiri Hills Nature Park & Punganoor Lake", "district": "Tirupattur", "category": "Nature & Plantations",
                "tags": ["hill_station", "lake", "boating", "nature", "cool_climate", "ghat"],
                "lat": 12.5786, "lng": 78.6369, "rating": 4.5, "review_count": 28000, "entry_fee_per_person": 30, "typical_duration_minutes": 120,
                "opening_time": "08:30", "closing_time": "18:00",
                "description": "Tranquil hill station lake surrounded by gardens, musical fountains, artificial cascades, and pedal boat tours at 1,110m elevation.",
                "best_time_to_visit": "Morning / Late Afternoon", "difficulty": "Easy", "is_mountain_route": True, "elevation_m": 1110
            },
            {
                "id": "poi_tpt_swamimalai_trek", "name": "Swamimalai Hill Peak Trek, Yelagiri", "district": "Tirupattur", "category": "Trekking",
                "tags": ["trekking", "highest_peak", "viewpoint", "clouds", "panoramic"],
                "lat": 12.5850, "lng": 78.6520, "rating": 4.6, "review_count": 14000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "06:00", "closing_time": "17:00",
                "description": "Trek to the highest point in Yelagiri Hills (4,338 ft) shaped like a cake, offering sweeping valley panoramas over the Eastern Ghats.",
                "best_time_to_visit": "Sunrise / Early Morning", "difficulty": "Moderate", "is_mountain_route": True, "elevation_m": 1322
            }
        ],
        [
            {
                "id": "hotel_tpt_cloud_nine", "name": "Yelagiri Hills Cloud Nine Resort", "district": "Tirupattur", "category": "Budget Hotel",
                "price_per_night": 1900, "rating": 4.4, "review_count": 980, "lat": 12.5760, "lng": 78.6380,
                "address": "Athanavoor, Yelagiri Hills", "amenities": ["Mountain View Balcony", "Campfire", "Homestyle Food", "Free Wi-Fi"],
                "room_type": "Pine View Cozy Cottage", "description": "Serene hillside retreat nestled in fruit orchards, featuring cool mountain breezes and campfire evenings."
            }
        ],
        [
            {
                "id": "food_tpt_ambur_star", "name": "Ambur Star Biryani Since 1890", "district": "Tirupattur", "category": "Local Food",
                "cuisine": "Traditional Ambur Dum Biryani", "specialties": ["Ambur Mutton Seeraga Samba Biryani", "Ennai Kathirikai (Brinjal Pachadi)", "Chicken 65", "Sweet Dhalcha"],
                "cost_for_two": 450, "rating": 4.8, "review_count": 38000, "lat": 12.7915, "lng": 78.7150, "opening_time": "11:00", "closing_time": "23:00",
                "description": "World-famous progenitor of Ambur-style biryani, slow-dum cooked with seeraga samba rice and marinated curd-based mutton."
            }
        ]
    )

    # 8. Tiruvannamalai
    add_district(
        "tiruvannamalai", "Tiruvannamalai", ["tiruvannamalai", "arunachala", "trinomali"], "Spiritual Central", "Tiruvannamalai", 12.2253, 79.0747, False, 171,
        "Spiritual powerhouse of South India, sacred home of Mount Arunachala representing the cosmic fire element (Agni Stalam), Sri Ramanasramam, and the grand Annamalaiyar temple complex.",
        ["Girivalam Herbal Pepper Soup", "Temple Sakkarai Pongal", "Red Rice Kozhukattai", "Sesame Milagu Thuvaiyal"],
        [
            {
                "id": "poi_tvm_annamalaiyar", "name": "Arulmigu Arunachaleswarar Temple (Agni Stalam)", "district": "Tiruvannamalai", "category": "Heritage",
                "tags": ["temple", "agni_stalam", "shiva", "pancha_bhoota", "gopuram"],
                "lat": 12.2319, "lng": 79.0677, "rating": 4.9, "review_count": 62000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "05:30", "closing_time": "21:30",
                "description": "One of India's largest Shaivite temple complexes covering 25 acres at the foot of Arunachala Hill, featuring four soaring gopurams including the 66-meter Raja Gopuram.",
                "best_time_to_visit": "Early Morning / Evening", "difficulty": "Easy"
            },
            {
                "id": "poi_tvm_girivalam_path", "name": "Sacred Arunachala Girivalam Path & 8 Lingams", "district": "Tiruvannamalai", "category": "Trekking",
                "tags": ["pilgrimage", "girivalam", "walk", "spiritual", "arunachala"],
                "lat": 12.2270, "lng": 79.0550, "rating": 4.9, "review_count": 35000, "entry_fee_per_person": 0, "typical_duration_minutes": 240,
                "opening_time": "04:00", "closing_time": "23:00",
                "description": "14-kilometer sacred circumambulation barefoot route around holy Mount Arunachala passing eight sacred cardinal lingam shrines.",
                "best_time_to_visit": "Dawn / Full Moon Night", "difficulty": "Moderate"
            }
        ],
        [
            {
                "id": "hotel_tvm_ramana_heritage", "name": "Arunachala Ramana Heritage Inn", "district": "Tiruvannamalai", "category": "Budget Hotel",
                "price_per_night": 1600, "rating": 4.5, "review_count": 1150, "lat": 12.2230, "lng": 79.0600,
                "address": "Chengham Road, Tiruvannamalai", "amenities": ["Arunachala Mountain View", "Pure Veg Dining", "Free Wi-Fi", "Meditation Hall"],
                "room_type": "Hill View Deluxe Room", "description": "Serene retreat with direct unobstructed views of the sacred Arunachala hill."
            }
        ],
        [
            {
                "id": "food_tvm_akshaya", "name": "Sri Akshaya Bhavan Pure Veg, Tiruvannamalai", "district": "Tiruvannamalai", "category": "Local Food",
                "cuisine": "Sattvic Tamil Vegetarian", "specialties": ["Ghee Pongal with Coconut Chutney", "Arunachala Herbal Rasam", "Steamed Idli Thali", "Filter Kaapi"],
                "cost_for_two": 220, "rating": 4.6, "review_count": 9400, "lat": 12.2280, "lng": 79.0650, "opening_time": "06:00", "closing_time": "22:00",
                "description": "Clean, uplifting sattvic eatery serving traditional South Indian meals without garlic or onion."
            }
        ]
    )

    # 9. Villupuram
    add_district(
        "villupuram", "Villupuram", ["villupuram", "gingee"], "Northern Central", "Villupuram", 11.9401, 79.4861, False, 42,
        "Historic heart of the impregnable Gingee Fort ('Troy of the East'), rocky boulder citadels, and ancient Jain rock-cut caverns.",
        ["Gingee Thattai Payaru Curry", "Villupuram Crispy Vadai", "Kambu Koozh with More Milagai"],
        [
            {
                "id": "poi_vpm_gingee_fort", "name": "Gingee Fort ('Troy of the East' - Rajagiri Citadel)", "district": "Villupuram", "category": "Heritage",
                "tags": ["fort", "rajagiri", "krishnagiri", "history", "trekking", "architecture"],
                "lat": 12.2505, "lng": 79.4184, "rating": 4.7, "review_count": 29000, "entry_fee_per_person": 25, "typical_duration_minutes": 180,
                "opening_time": "09:00", "closing_time": "17:30",
                "description": "Spectacular 13th-century mountain citadel atop a 240-meter sheer granite cliff with a wooden drawbridge, 7-story Kalyana Mahal, and granaries.",
                "best_time_to_visit": "Early Morning", "difficulty": "Moderate to Strenuous"
            }
        ],
        [
            {
                "id": "hotel_vpm_gingee_view", "name": "Gingee Fort View Residency", "district": "Villupuram", "category": "Budget Hotel",
                "price_per_night": 1400, "rating": 4.2, "review_count": 550, "lat": 12.2530, "lng": 79.4210,
                "address": "Tindivanam Road, Gingee", "amenities": ["Air Conditioning", "Free Parking", "Fort View Balcony"],
                "room_type": "Standard AC Room", "description": "Convenient basecamp located within sight of the dramatic Rajagiri citadel."
            }
        ],
        [
            {
                "id": "food_vpm_annapoorna", "name": "Annapoorna Veg Villupuram Junction", "district": "Villupuram", "category": "Local Food",
                "cuisine": "Traditional Tamil Veg", "specialties": ["Ghee Sambhar Vada", "Onion Uttapam", "Filter Coffee"],
                "cost_for_two": 200, "rating": 4.4, "review_count": 5200, "lat": 11.9410, "lng": 79.4880, "opening_time": "06:00", "closing_time": "22:30",
                "description": "Popular junction dining hall serving fresh steamed tiffins and piping hot filter coffee."
            }
        ]
    )

    # 10. Kallakurichi
    add_district(
        "kallakurichi", "Kallakurichi", ["kallakurichi", "kalvarayan"], "Kalvarayan Highlands", "Kallakurichi", 11.7384, 78.9639, True, 350,
        "Lush highland eco-tourism sanctuary anchored by the Kalvarayan Hills, roaring Megam falls, Gomukhi dam reservoir, and tribal spice plantations.",
        ["Kalvarayan Tapioca Vadai", "Forest Wild Honey & Millet Roti", "Nattu Kozhi Chukka"],
        [
            {
                "id": "poi_klk_megam_falls", "name": "Megam Falls & Periyar Falls, Kalvarayan Hills", "district": "Kallakurichi", "category": "Waterfalls",
                "tags": ["waterfall", "kalvarayan", "forest", "nature", "trekking"],
                "lat": 11.8500, "lng": 78.7800, "rating": 4.5, "review_count": 7800, "entry_fee_per_person": 10, "typical_duration_minutes": 120,
                "opening_time": "07:00", "closing_time": "17:30",
                "description": "Pristine tiered mountain cascades tumbling down forested granite gorges in the Kalvarayan hill range.",
                "best_time_to_visit": "Post-Monsoon / Morning", "difficulty": "Moderate", "is_mountain_route": True
            }
        ],
        [
            {
                "id": "hotel_klk_mist", "name": "Kalvarayan Mist Homestay", "district": "Kallakurichi", "category": "Budget Hotel",
                "price_per_night": 1300, "rating": 4.3, "review_count": 320, "lat": 11.8450, "lng": 78.7850,
                "address": "Kariamangalam Road, Kalvarayan Hills", "amenities": ["Campfire", "Homestyle Organic Food", "Mountain View"],
                "room_type": "Eco Hill Cottage", "description": "Tranquil hillside stay surrounded by pepper vines and fruit orchards."
            }
        ],
        [
            {
                "id": "food_klk_mess", "name": "Sri Lakshmi Mess Kallakurichi", "district": "Kallakurichi", "category": "Local Food",
                "cuisine": "Traditional Tamil Country Style", "specialties": ["Nattu Kozhi Kuzhambu", "Ragi Kali with Fish Curry", "Kallakurichi Parotta"],
                "cost_for_two": 260, "rating": 4.5, "review_count": 3900, "lat": 11.7400, "lng": 78.9650, "opening_time": "11:30", "closing_time": "22:00",
                "description": "Authentic rustic country mess renowned for wholesome stone-ground gravies."
            }
        ]
    )

    # 11. Cuddalore
    add_district(
        "cuddalore", "Cuddalore", ["cuddalore", "pichavaram", "chidambaram"], "Coastal Chola", "Cuddalore", 11.7480, 79.7714, False, 12,
        "Coastal heritage district home to the world's second-largest mangrove forest at Pichavaram, historic Silver Beach, and maritime estuaries.",
        ["Pichavaram Mangrove Crab Roast", "Cuddalore Coastal Fish Curry", "Steamed Idiyappam with Prawn Gravy"],
        [
            {
                "id": "poi_cud_pichavaram", "name": "Pichavaram Mangrove Forest & Boating", "district": "Cuddalore", "category": "Nature & Plantations",
                "tags": ["mangrove", "boating", "canal", "wetland", "nature", "biodiversity"],
                "lat": 11.4285, "lng": 79.7801, "rating": 4.6, "review_count": 36000, "entry_fee_per_person": 50, "typical_duration_minutes": 120,
                "opening_time": "08:00", "closing_time": "17:00",
                "description": "World's second largest mangrove ecosystem covering 1,100 hectares with 4,400 interconnected water channels navigated by rowboats under root canopies.",
                "best_time_to_visit": "Early Morning / Late Afternoon", "difficulty": "Easy"
            },
            {
                "id": "poi_cud_silver_beach", "name": "Silver Beach Devanampattinam", "district": "Cuddalore", "category": "Beaches",
                "tags": ["beach", "coast", "promenade", "horses", "sunset"],
                "lat": 11.7375, "lng": 79.7820, "rating": 4.3, "review_count": 14000, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "05:00", "closing_time": "21:00",
                "description": "Unspoiled 57-km coastal sand stretch on the Coromandel Coast with historic Fort St. David ruins nearby.",
                "best_time_to_visit": "Sunset", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_cud_mangrove_resort", "name": "Mangrove Eco Resort Pichavaram", "district": "Cuddalore", "category": "Budget Hotel",
                "price_per_night": 1800, "rating": 4.3, "review_count": 780, "lat": 11.4320, "lng": 79.7780,
                "address": "Pichavaram Boat Jetty Road, Chidambaram Taluk", "amenities": ["Canal View", "Boating Desk", "Seafood Restaurant"],
                "room_type": "Waterfront AC Cottage", "description": "Charming eco-resort situated right at the entrance of the Pichavaram mangrove waterways."
            }
        ],
        [
            {
                "id": "food_cud_coastal_catch", "name": "Coastal Catch Seafood Chidambaram / Cuddalore", "district": "Cuddalore", "category": "Local Food",
                "cuisine": "Coromandel Coastal Cuisine", "specialties": ["Spicy Mangrove Crab Masala", "Vanjaram Tawa Fry", "Meen Kuzhambu Meals"],
                "cost_for_two": 480, "rating": 4.6, "review_count": 8900, "lat": 11.4010, "lng": 79.6950, "opening_time": "11:30", "closing_time": "22:30",
                "description": "Celebrated for fresh estuarine fish and crab seasoned with black peppercorns and fennel."
            }
        ]
    )

    # 12. Salem
    add_district(
        "salem", "Salem", ["salem", "yercaud", "shevaroy"], "Kongu / Eastern Ghats", "Salem", 11.6643, 78.1460, True, 278,
        "Historic mango and steel capital nestled beneath the Shevaroy Hills, gateway to the tranquil Yercaud hill resort via 20 hairpin bends, and Mettur Dam reservoir.",
        ["Salem Thattu Vadai Settu (beetroot-carrot-chutney sandwich)", "Salem Malgova Mango Delights", "Kongu Parotta with Salna"],
        [
            {
                "id": "poi_slm_yercaud_lake", "name": "Yercaud Emerald Lake & Lady's Seat", "district": "Salem", "category": "Nature & Plantations",
                "tags": ["hill_station", "lake", "boating", "coffee", "viewpoint", "ghat"],
                "lat": 11.7753, "lng": 78.2093, "rating": 4.5, "review_count": 48000, "entry_fee_per_person": 30, "typical_duration_minutes": 120,
                "opening_time": "08:30", "closing_time": "18:00",
                "description": "'Jewel of the South' lake situated at 1,515m elevation surrounded by cloud-kissed coffee plantations, orange groves, and cliffside telescope overlooks.",
                "best_time_to_visit": "Morning / Sunset", "difficulty": "Easy", "is_mountain_route": True, "elevation_m": 1515
            },
            {
                "id": "poi_slm_kiliyur_falls", "name": "Kiliyur Waterfalls, Yercaud", "district": "Salem", "category": "Waterfalls",
                "tags": ["waterfall", "shevaroy", "trekking", "nature", "scenic"],
                "lat": 11.7960, "lng": 78.2030, "rating": 4.4, "review_count": 16000, "entry_fee_per_person": 20, "typical_duration_minutes": 105,
                "opening_time": "08:00", "closing_time": "17:00",
                "description": "300-foot waterfall dropping into the Servaroyan valley, reached via a rewarding forested stairway trek.",
                "best_time_to_visit": "Post-Monsoon", "difficulty": "Moderate", "is_mountain_route": True
            },
            {
                "id": "poi_slm_mettur_dam", "name": "Mettur Dam & Stanley Reservoir Park", "district": "Salem", "category": "Nature & Plantations",
                "tags": ["dam", "reservoir", "cauvery", "engineering", "gardens"],
                "lat": 11.7981, "lng": 77.8025, "rating": 4.4, "review_count": 22000, "entry_fee_per_person": 15, "typical_duration_minutes": 90,
                "opening_time": "09:00", "closing_time": "18:00",
                "description": "One of India's oldest multi-purpose masonry dams constructed in 1934 across the River Cauvery, featuring expansive landscaped parks and fish stalls.",
                "best_time_to_visit": "Late Afternoon", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_slm_grand_estancia", "name": "The Grand Estancia Salem", "district": "Salem", "category": "Budget Hotel",
                "price_per_night": 2500, "rating": 4.5, "review_count": 2400, "lat": 11.6720, "lng": 78.1380,
                "address": "Bangalore Bypass Road, Salem", "amenities": ["Swimming Pool", "Multi-Cuisine Restaurant", "Gym", "Free Wi-Fi"],
                "room_type": "Executive Deluxe Room", "description": "Sophisticated hotel offering easy access to Salem junction and the Yercaud ghat road entrance."
            }
        ],
        [
            {
                "id": "food_slm_thattu_vadai", "name": "Salem Famous Thattu Vadai Settu Corner", "district": "Salem", "category": "Local Food",
                "cuisine": "Kongu Street Food Delicacies", "specialties": ["Signature Thattu Vadai Settu", "Beetroot Onion Chutney Crisp", "Malgova Mango Shake", "Kalan Fry"],
                "cost_for_two": 150, "rating": 4.8, "review_count": 19000, "lat": 11.6620, "lng": 78.1510, "opening_time": "15:30", "closing_time": "22:30",
                "description": "Salem's iconic evening street snack: two crispy spiced rice discs sandwiched with grated beetroot, carrots, and secret tangy green sauce."
            }
        ]
    )

    # 13. Namakkal
    add_district(
        "namakkal", "Namakkal", ["namakkal", "kolli hills", "kolli"], "Kongu Highlands", "Namakkal", 11.2189, 78.1674, True, 1300,
        "Highland district crowned by the mythic Kolli Hills (famed for 70 hair-raising hairpin bends), the 300-ft Agaya Gangai waterfall, and the 18-ft monolithic Anjaneyar statue.",
        ["Kolli Hills Wild Honey Millets", "Namakkal Nattu Kozhi (Country Chicken) Pepper Fry", "Ragi Roti with Spicy Country Gravy"],
        [
            {
                "id": "poi_nmk_kolli_hills", "name": "Kolli Hills & Arapaleeswarar Temple (70 Hairpin Bends)", "district": "Namakkal", "category": "Nature & Plantations",
                "tags": ["hill_station", "70_hairpin_bends", "herbal", "adventure", "ghat", "temple"],
                "lat": 11.2500, "lng": 78.3400, "rating": 4.6, "review_count": 26000, "entry_fee_per_person": 0, "typical_duration_minutes": 180,
                "opening_time": "06:00", "closing_time": "19:00",
                "description": "Untouched Eastern Ghats mountain haven reached by an exhilarating 70 continuous hairpin road, famed for medicinal herbs and 1000-year-old Shiva temple.",
                "best_time_to_visit": "Morning", "difficulty": "Moderate", "is_mountain_route": True, "elevation_m": 1300
            },
            {
                "id": "poi_nmk_agaya_gangai", "name": "Agaya Gangai 300-Ft Waterfalls, Kolli Hills", "district": "Namakkal", "category": "Waterfalls",
                "tags": ["waterfall", "300ft", "steep_steps", "trekking", "river_aiyaru"],
                "lat": 11.2820, "lng": 78.3410, "rating": 4.6, "review_count": 15000, "entry_fee_per_person": 20, "typical_duration_minutes": 150,
                "opening_time": "07:00", "closing_time": "16:00",
                "description": "Roaring 300-foot waterfall cascading into a deep valley surrounded by cliffs, accessed via descending and climbing 1,050 stone steps.",
                "best_time_to_visit": "Morning", "difficulty": "Strenuous", "is_mountain_route": True
            },
            {
                "id": "poi_nmk_anjaneyar", "name": "Namakkal Fort & 18-Ft Monolithic Anjaneyar Temple", "district": "Namakkal", "category": "Heritage",
                "tags": ["fort", "monolith", "anjaneyar", "temple", "nayak"],
                "lat": 11.2223, "lng": 78.1678, "rating": 4.8, "review_count": 29000, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "06:30", "closing_time": "20:30",
                "description": "Massive single-stone 18-foot open-air idol of Lord Hanuman standing eye-to-eye with Lord Narasimha in Namakkal single rock fort.",
                "best_time_to_visit": "Morning / Evening", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_nmk_kolli_villa", "name": "Kolli Hills Green Valley Villa", "district": "Namakkal", "category": "Budget Hotel",
                "price_per_night": 1700, "rating": 4.3, "review_count": 640, "lat": 11.2520, "lng": 78.3420,
                "address": "Semmedu, Kolli Hills", "amenities": ["Valley Balcony", "Campfire", "Herbal Food", "Hot Water 24/7"],
                "room_type": "Mountain Mist Cottage", "description": "Quiet hilltop cottages surrounded by medicinal trees, offering cool climate and campfire evenings."
            }
        ],
        [
            {
                "id": "food_nmk_nattu_kozhi", "name": "Namakkal Nattu Kozhi Mess Since 1974", "district": "Namakkal", "category": "Local Food",
                "cuisine": "Traditional Kongu Non-Veg", "specialties": ["Country Chicken Pepper Chukka", "Nattu Kozhi Rasam", "Erode Manjal Biryani", "Ragi Kali"],
                "cost_for_two": 420, "rating": 4.7, "review_count": 13000, "lat": 11.2210, "lng": 78.1690, "opening_time": "11:30", "closing_time": "22:30",
                "description": "Celebrated across Tamil Nadu for free-range country chicken pan-fried in stone-ground black pepper and pure gingelly oil."
            }
        ]
    )

    # 14. Dharmapuri
    add_district(
        "dharmapuri", "Dharmapuri", ["dharmapuri", "hogenakkal"], "Kongu Border", "Dharmapuri", 12.1211, 78.1582, False, 468,
        "Famed for Hogenakkal Falls ('Niagara of India'), swirling coracle river voyages on the Cauvery gorge, therapeutic medicinal herbal river waters, and the sacred Theerthamalai shrine.",
        ["Hogenakkal Fresh Kaveri Fish Fry", "Dharmapuri Ragi Mudde with Naatu Kozhi Gravy", "Crispy Medu Vadai with Coconut Chutney"],
        [
            {
                "id": "poi_dmp_hogenakkal", "name": "Hogenakkal Falls & Coracle Boat Rides ('Niagara of India')", "district": "Dharmapuri", "category": "Waterfalls",
                "tags": ["waterfall", "coracle", "boating", "cauvery", "canyon", "herbal_bath"],
                "lat": 12.1188, "lng": 77.7766, "rating": 4.6, "review_count": 52000, "entry_fee_per_person": 50, "typical_duration_minutes": 180,
                "opening_time": "07:00", "closing_time": "17:30",
                "description": "Spectacular cascade where the Cauvery river splits into myriad roaring plumes cutting through ancient carbonatite rocks, celebrated for traditional round coracle boat navigation.",
                "best_time_to_visit": "Morning", "difficulty": "Easy to Moderate"
            }
        ],
        [
            {
                "id": "hotel_dmp_river_view", "name": "Hogenakkal River View Resort", "district": "Dharmapuri", "category": "Budget Hotel",
                "price_per_night": 1600, "rating": 4.2, "review_count": 890, "lat": 12.1220, "lng": 77.7800,
                "address": "Pennagaram Road, Hogenakkal", "amenities": ["River View", "Air Conditioning", "Fresh Fish Kitchen", "Boat Desk"],
                "room_type": "Deluxe River Facing Room", "description": "Comfortable riverside stay located five minutes from the main boat jetty."
            }
        ],
        [
            {
                "id": "food_dmp_kaveri_fish", "name": "Kaveri River Fish & Ragi Mess, Hogenakkal", "district": "Dharmapuri", "category": "Local Food",
                "cuisine": "Riverside Fresh Catch", "specialties": ["Crispy Tawa Kaveri Roghu Fry", "Spicy Fish Head Curry", "Ragi Mudde (Finger Millet Balls)", "Herbal Rasam"],
                "cost_for_two": 360, "rating": 4.6, "review_count": 16000, "lat": 12.1195, "lng": 77.7780, "opening_time": "08:00", "closing_time": "19:00",
                "description": "Authentic riverside shacks where freshly caught river fish is marinated in fiery hand-ground spices and fried right before you."
            }
        ]
    )

    # 15. Krishnagiri
    add_district(
        "krishnagiri", "Krishnagiri", ["krishnagiri", "hosur"], "Kongu Gateway", "Krishnagiri", 12.5186, 78.2137, False, 492,
        "Known as the mango bowl of Tamil Nadu, featuring Krishnagiri Dam reservoir gardens, historic Syed Basha mountain fort, and the industrial hub of Hosur.",
        ["Krishnagiri Fresh Mango Pulp Desserts", "Kaveripattinam Mutton Chukka", "Millet Adai with Jaggery Butter"],
        [
            {
                "id": "poi_krg_dam", "name": "Krishnagiri Dam & Reservoir Park", "district": "Krishnagiri", "category": "Nature & Plantations",
                "tags": ["dam", "reservoir", "gardens", "picnic", "mountains"],
                "lat": 12.4725, "lng": 78.1783, "rating": 4.4, "review_count": 14000, "entry_fee_per_person": 15, "typical_duration_minutes": 90,
                "opening_time": "09:00", "closing_time": "18:00",
                "description": "Scenic dam constructed across the Thenpennai river flanked by rugged granite hills, extensive green lawns, and flower beds.",
                "best_time_to_visit": "Late Afternoon", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_krg_daisy", "name": "Daisy Sky Inn Krishnagiri", "district": "Krishnagiri", "category": "Budget Hotel",
                "price_per_night": 1500, "rating": 4.3, "review_count": 670, "lat": 12.5210, "lng": 78.2160,
                "address": "Bangalore National Highway, Krishnagiri", "amenities": ["Free Wi-Fi", "Air Conditioning", "Highway Restaurant"],
                "room_type": "Standard AC Room", "description": "Comfortable highway hotel for travelers touring the Kongu gateway."
            }
        ],
        [
            {
                "id": "food_krg_highway", "name": "Highway Mango Kitchen Krishnagiri", "district": "Krishnagiri", "category": "Local Food",
                "cuisine": "Kongu & South Indian", "specialties": ["Mango Pachadi Thali", "Spicy Mutton Sukka", "Kari Dosai"],
                "cost_for_two": 320, "rating": 4.5, "review_count": 7200, "lat": 12.5190, "lng": 78.2140, "opening_time": "07:00", "closing_time": "22:30",
                "description": "Popular stopover featuring Kongu style gravies and seasonal mango delicacies."
            }
        ]
    )

    # 16. Erode
    add_district(
        "erode", "Erode", ["erode", "bhavani"], "Kongu Heart", "Erode", 11.3410, 77.7172, False, 183,
        "The turmeric capital of India ('Yellow City'), renowned for Bhavani Kooduthurai Triveni Sangam, Kodiveri waterfall dam, and authentic Pallipalayam chicken.",
        ["Erode Turmeric-Spiced Pallipalayam Chicken", "Kambu Koozh with More Milagai", "Kongu Santhakai (Steamed Rice String Hoppers)"],
        [
            {
                "id": "poi_erd_bhavani_sangam", "name": "Bhavani Kooduthurai (Triveni Sangam of TN)", "district": "Erode", "category": "Heritage",
                "tags": ["triveni_sangam", "river", "cauvery", "bhavani", "sangameswarar", "temple"],
                "lat": 11.4428, "lng": 77.6826, "rating": 4.7, "review_count": 31000, "entry_fee_per_person": 0, "typical_duration_minutes": 100,
                "opening_time": "05:30", "closing_time": "20:30",
                "description": "Sacred confluence where Cauvery, Bhavani, and the mystic subterranean Amutha rivers merge, watched over by the ancient Sangameswarar Temple.",
                "best_time_to_visit": "Early Morning", "difficulty": "Easy"
            },
            {
                "id": "poi_erd_kodiveri", "name": "Kodiveri Dam Waterfalls & Park", "district": "Erode", "category": "Waterfalls",
                "tags": ["waterfall", "dam", "bhavani", "bathing", "nature"],
                "lat": 11.5264, "lng": 77.3486, "rating": 4.4, "review_count": 22000, "entry_fee_per_person": 20, "typical_duration_minutes": 90,
                "opening_time": "08:30", "closing_time": "17:30",
                "description": "Historic stone weir built across the Bhavani River where cascading sheets of water provide refreshing river bathing beneath shady tamarind groves.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_erd_turmeric", "name": "Hotel Turmeric Erode", "district": "Erode", "category": "Budget Hotel",
                "price_per_night": 2100, "rating": 4.4, "review_count": 1400, "lat": 11.3450, "lng": 77.7210,
                "address": "Perundurai Road, Erode", "amenities": ["Air Conditioning", "Free Wi-Fi", "Traditional Restaurant", "Fitness Room"],
                "room_type": "Executive Double AC", "description": "Modern comfortable business and tourist hotel in the heart of Erode."
            }
        ],
        [
            {
                "id": "food_erd_pallipalayam", "name": "Pallipalayam Nattu Kozhi Mess, Erode", "district": "Erode", "category": "Local Food",
                "cuisine": "Authentic Kongu Non-Veg", "specialties": ["Signature Pallipalayam Chicken (cooked with garlic & red chillies)", "Kongu Parotta", "Mutton Brain Fry", "Koozh"],
                "cost_for_two": 380, "rating": 4.8, "review_count": 21000, "lat": 11.3520, "lng": 77.7280, "opening_time": "11:30", "closing_time": "22:30",
                "description": "The birthplace of Pallipalayam chicken—tender meat simmered without water using abundant shallots, garlic cloves, and broken dry red chillies."
            }
        ]
    )

    # 17. Tiruppur
    add_district(
        "tiruppur", "Tiruppur", ["tiruppur", "tirupur"], "Kongu Valley", "Tiruppur", 11.1085, 77.3411, False, 295,
        "Textile powerhouse of South India ('Knitwear Capital'), home to the scenic Thirumoorthy Hills, Amaravathi crocodile reserve, and authentic Arisi Paruppu Sadam.",
        ["Arisi Paruppu Sadam (classic Kongu one-pot lentil rice with ghee)", "Kangeyam Kaara Vadai", "Uthukuli Pure Butter Delights"],
        [
            {
                "id": "poi_tpr_thirumoorthy", "name": "Thirumoorthy Hills, Dam & Panjalinga Waterfalls", "district": "Tiruppur", "category": "Waterfalls",
                "tags": ["waterfall", "western_ghats", "temple", "dam", "scenic"],
                "lat": 10.4680, "lng": 77.1680, "rating": 4.6, "review_count": 24000, "entry_fee_per_person": 15, "typical_duration_minutes": 120,
                "opening_time": "06:00", "closing_time": "18:00",
                "description": "Scenic Western Ghats foothills harboring the Amanalingeswarar Temple (Trinity of Shiva, Vishnu & Brahma) and the mountain cascade of Panjalinga Falls.",
                "best_time_to_visit": "Morning", "difficulty": "Easy to Moderate"
            }
        ],
        [
            {
                "id": "hotel_tpr_poppys", "name": "Poppys Tower Tiruppur", "district": "Tiruppur", "category": "Budget Hotel",
                "price_per_night": 2300, "rating": 4.4, "review_count": 1250, "lat": 11.1120, "lng": 77.3450,
                "address": "Avinashi Road, Tiruppur", "amenities": ["Rooftop Restaurant", "Air Conditioning", "Free Breakfast", "Wi-Fi"],
                "room_type": "Superior King Room", "description": "Contemporary hotel with excellent connectivity to Avinashi temple and Kongu highway."
            }
        ],
        [
            {
                "id": "food_tpr_arisi_paruppu", "name": "Kongu Kitchen Arisi Paruppu Mess, Tiruppur", "district": "Tiruppur", "category": "Local Food",
                "cuisine": "Kongunadu Home Style", "specialties": ["Authentic Arisi Paruppu Sadam with Ghee", "Kangeyam Kaara Vadai", "Pachapuli Rasam", "Curd Vadai"],
                "cost_for_two": 220, "rating": 4.7, "review_count": 11000, "lat": 11.1090, "lng": 77.3420, "opening_time": "07:00", "closing_time": "21:30",
                "description": "Specializing in the quintessential Kongu comfort meal of turmeric-tinted rice and toor dal tempered with mustard, shallots, and fresh ghee."
            }
        ]
    )

    # 18. Coimbatore
    add_district(
        "coimbatore", "Coimbatore", ["coimbatore", "kovai", "kongu nadu"], "Kongu Nadu Capital", "Coimbatore", 11.0168, 76.9558, False, 411,
        "The textile and engineering powerhouse 'Manchester of South India', gateway to the Nilgiris, blessed with Siruvani sweet water, Adiyogi Shiva, and Annapoorna cuisine.",
        ["Sree Annapoorna Sambar Dosa", "Siruvani Filter Coffee", "Kongu Pallipalayam Chicken", "Kalan Masala (mushroom street snack)"],
        [
            {
                "id": "poi_cbe_adiyogi", "name": "112-Ft Adiyogi Shiva & Isha Yoga Center", "district": "Coimbatore", "category": "Heritage",
                "tags": ["adiyogi", "shiva", "monument", "yoga", "dhyanalinga", "scenic"],
                "lat": 10.9723, "lng": 76.7408, "rating": 4.9, "review_count": 92000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "Guinness World Record 112-foot steel bust of Adiyogi Shiva symbolizing the 112 ways to reach self-transformation, set against the dramatic Velliangiri Foothills.",
                "best_time_to_visit": "Late Afternoon / Evening (Light & Sound Show)", "difficulty": "Easy"
            },
            {
                "id": "poi_cbe_marudhamalai", "name": "Marudhamalai Hilltop Murugan Temple", "district": "Coimbatore", "category": "Heritage",
                "tags": ["temple", "hilltop", "murugan", "medicinal_plants", "panoramic"],
                "lat": 11.0456, "lng": 76.8522, "rating": 4.8, "review_count": 38000, "entry_fee_per_person": 0, "typical_duration_minutes": 90,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "12th-century hill shrine set amid Western Ghats medicinal shola flora, considered the 7th Padaiveedu of Lord Murugan.",
                "best_time_to_visit": "Morning / Evening", "difficulty": "Easy"
            },
            {
                "id": "poi_cbe_siruvani_falls", "name": "Siruvani Waterfalls & Dam (World's 2nd Sweetest Water)", "district": "Coimbatore", "category": "Waterfalls",
                "tags": ["waterfall", "siruvani", "nature", "forest", "pure_water"],
                "lat": 10.9630, "lng": 76.6910, "rating": 4.7, "review_count": 28000, "entry_fee_per_person": 50, "typical_duration_minutes": 120,
                "opening_time": "09:00", "closing_time": "15:00",
                "description": "Picturesque forest waterfall renowned worldwide for mineral-rich water rated the second sweetest on Earth, nestled within the dense Anaikatti forest reserve.",
                "best_time_to_visit": "Morning", "difficulty": "Moderate"
            }
        ],
        [
            {
                "id": "hotel_cbe_gokulam", "name": "Gokulam Park Coimbatore", "district": "Coimbatore", "category": "Budget Hotel",
                "price_per_night": 2600, "rating": 4.5, "review_count": 2100, "lat": 11.0520, "lng": 77.0120,
                "address": "Avinashi Road, Coimbatore", "amenities": ["Swimming Pool", "Multi-Cuisine Dining", "Wi-Fi", "Free Airport Shuttle"],
                "room_type": "Executive Suite", "description": "Well-appointed upscale hotel offering rapid transit to the Nilgiri foothills and city center."
            }
        ],
        [
            {
                "id": "food_cbe_annapoorna", "name": "Sree Annapoorna Sree Gowrishankar, Coimbatore", "district": "Coimbatore", "category": "Local Food",
                "cuisine": "Kongunadu & South Indian Vegetarian", "specialties": ["Legendary Ghee Roast Sambar Dosa", "Piping Hot Filter Kaapi", "Rava Upma with Chutney Trio", "Kongu Meals Thali"],
                "cost_for_two": 300, "rating": 4.8, "review_count": 48000, "lat": 11.0020, "lng": 76.9630, "opening_time": "06:00", "closing_time": "22:00",
                "description": "The gold standard of Tamil vegetarian dining, famed for its proprietary secret sambar recipe and world-class fresh chicory-tinted filter coffee."
            }
        ]
    )

    # 19. Nilgiris
    add_district(
        "nilgiris", "Nilgiris", ["nilgiris", "ooty", "coonoor", "kotagiri", "ootacamund"], "Western Ghats High Altitude", "Udhagamandalam (Ooty)", 11.4102, 76.6950, True, 2240,
        "The 'Blue Mountains' crowned by Doddabetta Peak (2,637 m), UNESCO mountain steam railway, rolling emerald tea estates, Toda tribal culture, and refreshing colonial hill sanctuaries.",
        ["Authentic Ooty Varkey (crisp flaky puff pastry)", "Steaming Nilgiri Orthodox Black Tea", "Toda Smoked Farm Cheese", "Homemade Dark Chocolate Fudge"],
        [
            {
                "id": "poi_nil_doddabetta", "name": "Doddabetta Peak & Telescope House, Ooty", "district": "Nilgiris", "category": "Nature & Plantations",
                "tags": ["viewpoint", "highest_peak", "nature", "tea", "photography", "ghat"],
                "lat": 11.4010, "lng": 76.7356, "rating": 4.6, "review_count": 52000, "entry_fee_per_person": 30, "typical_duration_minutes": 90,
                "opening_time": "09:00", "closing_time": "18:00",
                "description": "Highest mountain in the Nilgiri Hills (2,637 m / 8,652 ft) offering panoramic 360-degree views across misty shola forests, valleys, and distant plains.",
                "best_time_to_visit": "Morning", "difficulty": "Easy", "is_mountain_route": True, "elevation_m": 2637
            },
            {
                "id": "poi_nil_pykara_falls", "name": "Pykara Waterfalls & Boating Reservoir", "district": "Nilgiris", "category": "Waterfalls",
                "tags": ["waterfall", "boating", "lake", "scenic", "pine_forest", "ghat"],
                "lat": 11.4552, "lng": 76.6021, "rating": 4.6, "review_count": 31000, "entry_fee_per_person": 60, "typical_duration_minutes": 105,
                "opening_time": "08:30", "closing_time": "17:30",
                "description": "Sacred Toda river tumbling over two tiers of granite ledges into a tranquil mountain reservoir equipped with TTDC speedboats.",
                "best_time_to_visit": "Midday", "difficulty": "Easy to Moderate", "is_mountain_route": True, "elevation_m": 2180
            },
            {
                "id": "poi_nil_botanical_garden", "name": "Government Botanical Garden & Rose Garden, Ooty", "district": "Nilgiris", "category": "Nature & Plantations",
                "tags": ["garden", "flowers", "fossil_tree", "heritage", "cool_climate"],
                "lat": 11.4191, "lng": 76.7118, "rating": 4.5, "review_count": 68000, "entry_fee_per_person": 40, "typical_duration_minutes": 90,
                "opening_time": "07:00", "closing_time": "18:30",
                "description": "Colonial garden founded in 1848 terraced across 55 acres, showcasing over 1,000 exotic floral species and a 20-million-year-old fossilized tree trunk.",
                "best_time_to_visit": "Morning", "difficulty": "Easy", "is_mountain_route": True, "elevation_m": 2240
            },
            {
                "id": "poi_nil_toy_train", "name": "UNESCO Nilgiri Mountain Railway (Ooty - Coonoor Toy Train)", "district": "Nilgiris", "category": "Heritage",
                "tags": ["unesco", "toy_train", "steam_engine", "heritage", "scenic", "tunnels"],
                "lat": 11.4080, "lng": 76.7020, "rating": 4.9, "review_count": 42000, "entry_fee_per_person": 150, "typical_duration_minutes": 120,
                "opening_time": "07:10", "closing_time": "18:00",
                "description": "UNESCO World Heritage meter-gauge rack-and-pinion steam railway traversing 16 tunnels, 250 bridges, and deep river ravines through cloud-capped tea valleys.",
                "best_time_to_visit": "Morning Departure", "difficulty": "Easy", "is_mountain_route": True
            }
        ],
        [
            {
                "id": "hotel_nil_mist_cottage", "name": "Nilgiri Mist Valley Homestay, Ooty", "district": "Nilgiris", "category": "Budget Hotel",
                "price_per_night": 1700, "rating": 4.5, "review_count": 1280, "lat": 11.4110, "lng": 76.7230,
                "address": "Fern Hill Road, Ooty", "amenities": ["Mountain View Balcony", "Hot Water 24/7", "Campfire", "Homestyle Tea"],
                "room_type": "Pine View Cozy Cottage", "description": "Serene colonial-style cottage bordered by eucalyptus groves, offering home-cooked Nilgiri meals and fireplace warmth."
            }
        ],
        [
            {
                "id": "food_nil_varkey_lounge", "name": "Westly's Nilgiri Varkey & Tea Room, Ooty", "district": "Nilgiris", "category": "Local Food",
                "cuisine": "Colonial Nilgiri Tea & Bakery", "specialties": ["Crisp Flaky Ooty Varkey (straight from wood-fired oven)", "Highland Orange Pekoe Tea", "Homemade Hot Chocolate", "Plum Cake"],
                "cost_for_two": 180, "rating": 4.8, "review_count": 22000, "lat": 11.4120, "lng": 76.7050, "opening_time": "07:30", "closing_time": "21:00",
                "description": "The quintessential Ooty experience: dipping warm, flaky varkey pastry into fresh Nilgiri orthodox tea while watching mountain mist roll over the peaks."
            }
        ]
    )

    # 20. Karur
    add_district(
        "karur", "Karur", ["karur"], "Kongu River Valley", "Karur", 10.9601, 78.0766, False, 101,
        "Historic Chera dynasty capital on the banks of River Amaravathi, celebrated for the 2000-year-old Pasupatheeswarar temple, textile handlooms, and Mayanur barrage.",
        ["Karur Pure Ghee Pongal", "Amaravathi River Meen Varuval", "Karur Murukku"],
        [
            {
                "id": "poi_kar_pasupatheeswarar", "name": "Sri Pasupatheeswarar Ancient Chola Temple", "district": "Karur", "category": "Heritage",
                "tags": ["temple", "chera", "chola", "shiva", "stone_inscriptions"],
                "lat": 10.9592, "lng": 78.0833, "rating": 4.7, "review_count": 14000, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "Ancient Shiva shrine built by the Cholas with inscriptions dating back to 1st century BCE, featuring a 5-foot swayambhu lingam with hoof marks.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_kar_residency", "name": "The Residency Karur", "district": "Karur", "category": "Budget Hotel",
                "price_per_night": 1800, "rating": 4.3, "review_count": 820, "lat": 10.9620, "lng": 78.0790,
                "address": "Covai Road, Karur", "amenities": ["Air Conditioning", "Free Parking", "Veg Restaurant"],
                "room_type": "Executive Double Room", "description": "Reliable, well-maintained hotel for tourists and business travelers."
            }
        ],
        [
            {
                "id": "food_kar_shanthi", "name": "Sree Shanthi Mess Karur", "district": "Karur", "category": "Local Food",
                "cuisine": "Traditional Kongu Cuisine", "specialties": ["Ghee Pongal with Chutney", "Amaravathi Fish Curry", "Banana Leaf Meals"],
                "cost_for_two": 220, "rating": 4.5, "review_count": 4800, "lat": 10.9610, "lng": 78.0780, "opening_time": "06:30", "closing_time": "22:00",
                "description": "Wholesome Kongu vegetarian and non-vegetarian fare served on fresh plantain leaves."
            }
        ]
    )

    # 21. Tiruchirappalli (Trichy)
    add_district(
        "tiruchirappalli", "Tiruchirappalli", ["tiruchirappalli", "trichy", "srirangam"], "Chola Nadu Central", "Tiruchirappalli", 10.7905, 78.7047, False, 88,
        "Historic heart of Tamil Nadu crowned by Sri Ranganathaswamy Temple at Srirangam (world's largest functioning temple complex), Rockfort Ucchi Pillayar temple, and Grand Anicut.",
        ["GI-Tagged Manapparai Murukku", "Trichy Banana Leaf Thali", "Srirangam Puliyodharai", "Ghee Roast Dosa"],
        [
            {
                "id": "poi_tri_srirangam", "name": "Sri Ranganathaswamy Temple, Srirangam", "district": "Tiruchirappalli", "category": "Heritage",
                "tags": ["temple", "largest_temple", "unesco", "vaishnava", "gopuram", "heritage"],
                "lat": 10.8623, "lng": 78.6901, "rating": 4.9, "review_count": 76000, "entry_fee_per_person": 0, "typical_duration_minutes": 180,
                "opening_time": "06:00", "closing_time": "21:00",
                "description": "Massive 156-acre river-island temple complex with 21 grand gopurams including the 73-meter Rajagopuram, 39 pavilions, and 50 sub-shrines.",
                "best_time_to_visit": "Early Morning", "difficulty": "Easy to Moderate"
            },
            {
                "id": "poi_tri_rockfort", "name": "Rockfort Ucchi Pillayar Temple (437 Stone Steps)", "district": "Tiruchirappalli", "category": "Heritage",
                "tags": ["rockfort", "ganesha", "climb", "panoramic", "heritage"],
                "lat": 10.8284, "lng": 78.6967, "rating": 4.8, "review_count": 48000, "entry_fee_per_person": 10, "typical_duration_minutes": 105,
                "opening_time": "06:00", "closing_time": "20:00",
                "description": "Historic fortress perched atop an 83-meter ancient monolithic rock (older than the Himalayas at 3.8 billion years), climbing 437 steps to an eagle-eye panoramic view.",
                "best_time_to_visit": "Sunrise / Sunset", "difficulty": "Moderate"
            },
            {
                "id": "poi_tri_kallanai", "name": "Kallanai Dam (Grand Anicut Built 2nd Century CE)", "district": "Tiruchirappalli", "category": "Heritage",
                "tags": ["dam", "chola", "karikala", "ancient_engineering", "cauvery"],
                "lat": 10.8329, "lng": 78.8188, "rating": 4.6, "review_count": 28000, "entry_fee_per_person": 15, "typical_duration_minutes": 75,
                "opening_time": "08:00", "closing_time": "18:00",
                "description": "World's fourth-oldest water-diversion dam still in operational use, built by King Karikala Chola across the unharnessed Cauvery river.",
                "best_time_to_visit": "Late Afternoon", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_tri_gardenia", "name": "Grand Gardenia Trichy Central", "district": "Tiruchirappalli", "category": "Budget Hotel",
                "price_per_night": 2200, "rating": 4.4, "review_count": 1850, "lat": 10.7980, "lng": 78.6870,
                "address": "Collector Office Road, Cantonment, Trichy", "amenities": ["Free Wi-Fi", "Air Conditioning", "Rooftop Restaurant", "Airport Shuttle"],
                "room_type": "Executive Double AC", "description": "Centrally placed hotel offering quick access to Rockfort, Srirangam island, and the airport."
            }
        ],
        [
            {
                "id": "food_tri_sangeethas", "name": "Sri Sangeethas Veg Central, Trichy", "district": "Tiruchirappalli", "category": "Local Food",
                "cuisine": "Traditional South Indian Vegetarian", "specialties": ["Ghee Roast Dosa", "Manapparai Crunchy Murukku Platter", "Srirangam Temple Puliyodharai", "Thali Meals"],
                "cost_for_two": 280, "rating": 4.7, "review_count": 32000, "lat": 10.7920, "lng": 78.6910, "opening_time": "06:00", "closing_time": "22:30",
                "description": "Legendary Trichy dining brand serving banana leaf vegetarian meals and authentic GI-tagged Manapparai murukku."
            }
        ]
    )

    # 22. Thanjavur
    add_district(
        "thanjavur", "Thanjavur", ["thanjavur", "tanjore", "kumbakonam"], "Chola Nadu Heart", "Thanjavur", 10.7870, 79.1378, False, 57,
        "The glorious cradle of Tamil classical art, music, and bronze casting, anchored by the UNESCO World Heritage Brihadisvara Temple ('Big Temple') and Kumbakonam temples.",
        ["Kumbakonam Degree Filter Kaapi", "Thanjavur Kadappa (potato-moong dal gravy)", "Thanjavur Ash Gourd Kootu", "Thirunageswaram Halwa"],
        [
            {
                "id": "poi_thj_brihadisvara", "name": "Brihadisvara Temple (UNESCO 'Big Temple')", "district": "Thanjavur", "category": "Heritage",
                "tags": ["unesco", "chola", "architecture", "rajaraja", "monolith", "heritage"],
                "lat": 10.7828, "lng": 79.1318, "rating": 4.9, "review_count": 89000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "Architectural marvel consecrated in 1010 CE by King Raja Raja Chola I, featuring a 66-meter granite vimana crowned with an 80-tonne monolithic cupola that casts no midday shadow.",
                "best_time_to_visit": "Early Morning / Golden Hour (Lit up)", "difficulty": "Easy"
            },
            {
                "id": "poi_thj_maratha_palace", "name": "Thanjavur Maratha Royal Palace & Saraswathi Mahal Library", "district": "Thanjavur", "category": "Heritage",
                "tags": ["palace", "maratha", "manuscripts", "museum", "bronzes"],
                "lat": 10.7925, "lng": 79.1367, "rating": 4.5, "review_count": 26000, "entry_fee_per_person": 50, "typical_duration_minutes": 105,
                "opening_time": "09:00", "closing_time": "17:30",
                "description": "16th-century palace complex of the Nayak and Maratha rulers housing world-famous Chola bronzes and the Saraswathi Mahal Library holding 60,000 ancient palm-leaf manuscripts.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_thj_gnanam", "name": "Hotel Gnanam Thanjavur", "district": "Thanjavur", "category": "Budget Hotel",
                "price_per_night": 1900, "rating": 4.4, "review_count": 1650, "lat": 10.7890, "lng": 79.1350,
                "address": "Gandhi Road, Thanjavur", "amenities": ["Air Conditioning", "Free Wi-Fi", "Veg Restaurant", "Tour Desk"],
                "room_type": "Deluxe AC Room", "description": "Highly regarded heritage city stay walking distance to the Big Temple and royal palace."
            }
        ],
        [
            {
                "id": "food_thj_degree_coffee", "name": "Murali's Kumbakonam Degree Coffee & Mess, Thanjavur", "district": "Thanjavur", "category": "Local Food",
                "cuisine": "Traditional Chola Nadu Tiffin", "specialties": ["Authentic Cow Milk Degree Filter Kaapi", "Kadappa with Steamed Idli", "Vazhaipoo Vadai", "Kasi Halwa"],
                "cost_for_two": 190, "rating": 4.8, "review_count": 24000, "lat": 10.7850, "lng": 79.1330, "opening_time": "06:00", "closing_time": "22:00",
                "description": "Pure cow-milk degree coffee frothed into brass dabarah sets, accompanying hot spongy idlis served with spicy fennel Kadappa."
            }
        ]
    )

    # 23. Ariyalur
    add_district(
        "ariyalur", "Ariyalur", ["ariyalur", "gangaikonda cholapuram"], "Chola Heritage", "Ariyalur", 11.1401, 79.0786, False, 76,
        "Imperial Chola heartland harboring the UNESCO World Heritage Brihadisvara temple at Gangaikonda Cholapuram built by King Rajendra Chola I, and prehistoric Cretaceous fossil beds.",
        ["Kollidam Fresh Meen Kulambu", "Milagu Rasam Thali", "Crispy Medu Vadai with Coconut Chutney"],
        [
            {
                "id": "poi_ari_gangaikonda", "name": "Gangaikonda Cholapuram (UNESCO Brihadisvara Temple)", "district": "Ariyalur", "category": "Heritage",
                "tags": ["unesco", "chola", "rajendra_chola", "architecture", "sculptures"],
                "lat": 11.2062, "lng": 79.4533, "rating": 4.8, "review_count": 34000, "entry_fee_per_person": 25, "typical_duration_minutes": 120,
                "opening_time": "06:00", "closing_time": "18:30",
                "description": "UNESCO World Heritage temple constructed in 1035 CE by Emperor Rajendra Chola I to commemorate his victorious military expedition to the sacred River Ganges.",
                "best_time_to_visit": "Morning / Late Afternoon", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_ari_heritage", "name": "Chola Heritage Regency Ariyalur", "district": "Ariyalur", "category": "Budget Hotel",
                "price_per_night": 1400, "rating": 4.2, "review_count": 420, "lat": 11.1420, "lng": 79.0810,
                "address": "Jayankondam Road, Ariyalur", "amenities": ["Air Conditioning", "Free Parking", "Veg Restaurant"],
                "room_type": "Standard Deluxe Room", "description": "Comfortable stay for history buffs exploring Chola monuments and fossil grounds."
            }
        ],
        [
            {
                "id": "food_ari_mess", "name": "Sri Venkateshwara Mess Jayankondam", "district": "Ariyalur", "category": "Local Food",
                "cuisine": "Traditional Chola Nadu Cuisine", "specialties": ["Banana Leaf Meals with Kollidam Fish", "Milagu Rasam", "Curd Vadai"],
                "cost_for_two": 240, "rating": 4.5, "review_count": 3800, "lat": 11.2100, "lng": 79.4490, "opening_time": "11:30", "closing_time": "21:30",
                "description": "Home-style country mess serving authentic regional fish curries and piping hot rasam."
            }
        ]
    )

    # 24. Perambalur
    add_district(
        "perambalur", "Perambalur", ["perambalur", "ranjankudi"], "Central Mineral Belt", "Perambalur", 11.2333, 78.8824, False, 114,
        "Historic crossroads featuring the 17th-century Ranjankudi Nayaka fort, Chettikulam temple, and Pachamalai hills eco-trails.",
        ["Perambalur Millet Kozhukattai", "Naatu Thuvaiyal Thali", "Parotta with Chicken Salna"],
        [
            {
                "id": "poi_pbl_ranjankudi", "name": "Ranjankudi Fort (17th-Century Nayaka Stronghold)", "district": "Perambalur", "category": "Heritage",
                "tags": ["fort", "nayak", "carnatic_wars", "history", "architecture"],
                "lat": 11.3653, "lng": 78.9667, "rating": 4.4, "review_count": 6800, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "08:00", "closing_time": "18:00",
                "description": "Massive stone fortress with three tiers of stone battlements that witnessed the Battle of Valikondah in 1751 during the Carnatic Wars.",
                "best_time_to_visit": "Morning / Evening", "difficulty": "Easy to Moderate"
            }
        ],
        [
            {
                "id": "hotel_pbl_maya", "name": "Maya Hotel Perambalur", "district": "Perambalur", "category": "Budget Hotel",
                "price_per_night": 1350, "rating": 4.2, "review_count": 510, "lat": 11.2360, "lng": 78.8850,
                "address": "Trichy-Chennai Highway, Perambalur", "amenities": ["Air Conditioning", "Free Parking", "Restaurant"],
                "room_type": "Standard AC Room", "description": "Clean, practical transit basecamp on the Trichy-Chennai national highway."
            }
        ],
        [
            {
                "id": "food_pbl_annapoorna", "name": "Annapoorna Grand Highway Perambalur", "district": "Perambalur", "category": "Local Food",
                "cuisine": "Traditional Tamil Cuisine", "specialties": ["Ghee Roast Dosa", "Vegetarian Thali", "Filter Kaapi"],
                "cost_for_two": 220, "rating": 4.4, "review_count": 4200, "lat": 11.2340, "lng": 78.8830, "opening_time": "06:30", "closing_time": "22:30",
                "description": "Reliable highway restaurant providing clean, wholesome meals and quick service."
            }
        ]
    )

    # 25. Pudukkottai
    add_district(
        "pudukkottai", "Pudukkottai", ["pudukkottai", "sittanavasal"], "Tondaiman Royal Principality", "Pudukkottai", 10.3797, 78.8208, False, 100,
        "Historic princely state famed for 2nd-century BCE Sittanavasal rock-cut Jain murals, Thirumayam boulder fort, and grand Avudaiyarkoil shrine.",
        ["Pudukkottai Muttai Parotta", "Kandarvakkottai Milagu Roast", "Chettinad Touch Vadai"],
        [
            {
                "id": "poi_pud_sittanavasal", "name": "Sittanavasal 2nd-Century BCE Jain Cave & Fresco Murals", "district": "Pudukkottai", "category": "Heritage",
                "tags": ["jain", "frescoes", "paintings", "cave", "ancient", "monolith"],
                "lat": 10.4578, "lng": 78.7303, "rating": 4.7, "review_count": 18000, "entry_fee_per_person": 25, "typical_duration_minutes": 100,
                "opening_time": "09:00", "closing_time": "17:30",
                "description": "Ancient monolithic rock-cut cave containing exquisite natural vegetable-dye fresco paintings of lotus tanks and dancing apsaras, rivaling Ajanta caves.",
                "best_time_to_visit": "Morning", "difficulty": "Easy to Moderate"
            },
            {
                "id": "poi_pud_thirumayam", "name": "Thirumayam Rock-Cut Fort & Perumal Cave", "district": "Pudukkottai", "category": "Heritage",
                "tags": ["fort", "rock_cut", "perumal", "shiva", "panoramic"],
                "lat": 10.2483, "lng": 78.7525, "rating": 4.5, "review_count": 11000, "entry_fee_per_person": 25, "typical_duration_minutes": 90,
                "opening_time": "08:00", "closing_time": "18:00",
                "description": "Historic 40-acre fortress built atop a granite boulder by King Sethupathi of Ramanathapuram, with rock-cut shrines to Lord Vishnu and Lord Shiva.",
                "best_time_to_visit": "Morning / Late Afternoon", "difficulty": "Easy to Moderate"
            }
        ],
        [
            {
                "id": "hotel_pud_heritage", "name": "Chidambara Vilas Heritage Gateway", "district": "Pudukkottai", "category": "Budget Hotel",
                "price_per_night": 2300, "rating": 4.6, "review_count": 920, "lat": 10.3850, "lng": 78.8250,
                "address": "Tirumayam Road, Pudukkottai", "amenities": ["Heritage Courtyard", "Air Conditioning", "Traditional Cuisine", "Free Wi-Fi"],
                "room_type": "Heritage Double Room", "description": "Authentic architectural stay with antique woodwork and royal princely decor."
            }
        ],
        [
            {
                "id": "food_pud_royal_mess", "name": "Royal Mess Pudukkottai", "district": "Pudukkottai", "category": "Local Food",
                "cuisine": "Traditional Pudukkottai & Chettinad", "specialties": ["Signature Muttai Parotta", "Nattu Kozhi Chukka", "Kari Dosa"],
                "cost_for_two": 320, "rating": 4.6, "review_count": 7800, "lat": 10.3810, "lng": 78.8220, "opening_time": "12:00", "closing_time": "22:30",
                "description": "Famed for flaky shredded egg parotta tossed on hot iron griddles with roasted shallots."
            }
        ]
    )

    # 26. Dindigul
    add_district(
        "dindigul", "Dindigul", ["dindigul", "kodaikanal", "kodai"], "South Central / Western Ghats", "Dindigul", 10.3673, 77.9803, True, 2133,
        "Renowned for the misty 'Princess of Hill Stations' Kodaikanal (at 2,133 m elevation), historic Dindigul Rock Fort, and legendary Seeraga Samba Biryani.",
        ["Dindigul Thalappakatti Seeraga Samba Mutton Biryani", "Kodaikanal Homemade Fruit Chocolates", "Kodai Cheese & Fresh Pears"],
        [
            {
                "id": "poi_dgl_kodai_lake", "name": "Kodaikanal Star-Shaped Lake & Coaker's Walk", "district": "Dindigul", "category": "Nature & Plantations",
                "tags": ["lake", "boating", "hill_station", "coakers_walk", "viewpoint", "mist", "ghat"],
                "lat": 10.2381, "lng": 77.4892, "rating": 4.7, "review_count": 74000, "entry_fee_per_person": 50, "typical_duration_minutes": 150,
                "opening_time": "08:30", "closing_time": "18:00",
                "description": "Iconic artificial star-shaped lake created in 1863 set amidst pine hills, flanked by Coaker's Walk—a 1-km cliffside pedestrian promenade over misty valleys.",
                "best_time_to_visit": "Morning / Late Afternoon", "difficulty": "Easy", "is_mountain_route": True, "elevation_m": 2133
            },
            {
                "id": "poi_dgl_pillar_rocks", "name": "Pillar Rocks & Guna Caves (Devil's Kitchen)", "district": "Dindigul", "category": "Nature & Plantations",
                "tags": ["pillar_rocks", "caves", "cliffs", "mist", "panoramic", "ghat"],
                "lat": 10.2104, "lng": 77.4682, "rating": 4.6, "review_count": 45000, "entry_fee_per_person": 30, "typical_duration_minutes": 90,
                "opening_time": "09:00", "closing_time": "17:30",
                "description": "Three vertical granite rock pillars standing 122 meters high jutting into cloud-filled canyons, adjacent to ancient moss-draped deep caves.",
                "best_time_to_visit": "Morning", "difficulty": "Easy", "is_mountain_route": True, "elevation_m": 2200
            },
            {
                "id": "poi_dgl_silver_cascade", "name": "Silver Cascade Falls, Kodaikanal Ghat", "district": "Dindigul", "category": "Waterfalls",
                "tags": ["waterfall", "ghat_road", "scenic", "stream", "nature"],
                "lat": 10.2520, "lng": 77.5250, "rating": 4.4, "review_count": 28000, "entry_fee_per_person": 0, "typical_duration_minutes": 45,
                "opening_time": "06:00", "closing_time": "18:30",
                "description": "Sparkling 55-meter waterfall tumbling over steep rocks directly alongside the main Kodaikanal-Batlagundu ghat road.",
                "best_time_to_visit": "Midday", "difficulty": "Easy", "is_mountain_route": True
            }
        ],
        [
            {
                "id": "hotel_dgl_kodai_pine", "name": "Kodai Pine Haven Inn, Kodaikanal", "district": "Dindigul", "category": "Budget Hotel",
                "price_per_night": 1650, "rating": 4.4, "review_count": 1150, "lat": 10.2340, "lng": 77.4910,
                "address": "Lake Road, Kodaikanal", "amenities": ["Lake View", "Free Wi-Fi", "Heater on Request", "Travel Desk"],
                "room_type": "Standard Lake Facing Room", "description": "Budget lakeside stay offering quiet surroundings, cycling rentals, and rapid access to Coaker's Walk."
            }
        ],
        [
            {
                "id": "food_dgl_thalappakatti", "name": "Dindigul Thalappakatti Authentic Biryani Since 1957", "district": "Dindigul", "category": "Local Food",
                "cuisine": "Traditional Tamil Non-Veg & Seeraga Samba", "specialties": ["Seeraga Samba Mutton Biryani", "Ennai Kathirikai Curry", "Mutton Sukka Varuval", "Egg Biryani"],
                "cost_for_two": 520, "rating": 4.8, "review_count": 44000, "lat": 10.3650, "lng": 77.9780, "opening_time": "11:30", "closing_time": "23:00",
                "description": "The founding birthplace of Thalappakatti biryani—fragrant short-grain Seeraga Samba rice slow-dum cooked with tender Kannivadi meat and stone-ground spices."
            }
        ]
    )

    # 27. Theni
    add_district(
        "theni", "Theni", ["theni", "meghamalai", "suruli", "cumbum"], "Cardamom Highlands", "Theni", 10.0104, 77.4768, True, 1500,
        "Valley of green abundance at the foot of the Western Ghats, celebrated for Suruli falls, Meghamalai Highwavys cloud forest, and lush Cumbum grape vineyards.",
        ["Cumbum Valley Fresh Paneer Grapes & Juice", "Suruli Herb-Infused Mutton Chukka", "Parotta with Chicken Salna"],
        [
            {
                "id": "poi_the_suruli_falls", "name": "Suruli Waterfalls & 18 Natural Caves", "district": "Theni", "category": "Waterfalls",
                "tags": ["waterfall", "caves", "ayurvedic", "forest", "nature"],
                "lat": 9.6644, "lng": 77.2917, "rating": 4.6, "review_count": 28000, "entry_fee_per_person": 20, "typical_duration_minutes": 120,
                "opening_time": "07:00", "closing_time": "17:00",
                "description": "Famous two-stage waterfall mentioned in the ancient epic Silappadikaram, cascading through 18 natural rock caves with herbal-rich healing water.",
                "best_time_to_visit": "Morning", "difficulty": "Easy to Moderate"
            },
            {
                "id": "poi_the_meghamalai", "name": "Meghamalai ('Highwavys' Cloud Mountain)", "district": "Theni", "category": "Nature & Plantations",
                "tags": ["cloud_mountain", "tea_estates", "wildlife", "ghat", "cool_climate", "panoramic"],
                "lat": 9.7100, "lng": 77.4000, "rating": 4.7, "review_count": 18000, "entry_fee_per_person": 0, "typical_duration_minutes": 240,
                "opening_time": "06:00", "closing_time": "18:00",
                "description": "High-altitude tea estate mountain range at 1,500m shrouded in perpetual mist, offering encounters with wild elephants and Nilgiri tahrs.",
                "best_time_to_visit": "Morning", "difficulty": "Moderate", "is_mountain_route": True, "elevation_m": 1500
            }
        ],
        [
            {
                "id": "hotel_the_cloud", "name": "Cloud Mountain Homestay Meghamalai", "district": "Theni", "category": "Budget Hotel",
                "price_per_night": 1850, "rating": 4.5, "review_count": 520, "lat": 9.7150, "lng": 77.4050,
                "address": "Highwavys Estate, Meghamalai", "amenities": ["Tea Estate View", "Campfire", "Homestyle Food", "Hot Water"],
                "room_type": "Tea Plantation Cottage", "description": "Serene homestay surrounded by rolling tea bushes and cool mountain breezes."
            }
        ],
        [
            {
                "id": "food_the_green_valley", "name": "Green Valley Restaurant Theni", "district": "Theni", "category": "Local Food",
                "cuisine": "Traditional Cumbum Valley Cuisine", "specialties": ["Fresh Cumbum Grape Juice", "Nattu Kozhi Chukka", "Parotta with Salna"],
                "cost_for_two": 280, "rating": 4.5, "review_count": 6400, "lat": 10.0120, "lng": 77.4780, "opening_time": "07:00", "closing_time": "22:00",
                "description": "Popular stopover serving farm-fresh grape juice and authentic South Tamil non-vegetarian delicacies."
            }
        ]
    )

    # 28. Madurai
    add_district(
        "madurai", "Madurai", ["madurai"], "Pandiya Nadu Capital", "Madurai", 9.9252, 78.1198, False, 101,
        "The ancient soul of Tamil culture ('Thoonga Nagaram' - City That Never Sleeps), home to the world-renowned Meenakshi Amman Temple, Thirumalai Nayakkar Palace, and iconic Jigarthanda.",
        ["Madurai Special Famous Jigarthanda (almond gum, nannari & cream)", "Murugan Idli with 4 Chutneys", "Madurai Kari Dosa (minced mutton pancake)", "Bun Parotta with Salna"],
        [
            {
                "id": "poi_mdu_meenakshi", "name": "Meenakshi Amman Temple, Madurai", "district": "Madurai", "category": "Heritage",
                "tags": ["temple", "heritage", "dravidian", "gopuram", "unesco", "thousand_pillars"],
                "lat": 9.9195, "lng": 78.1193, "rating": 4.9, "review_count": 88000, "entry_fee_per_person": 50, "typical_duration_minutes": 150,
                "opening_time": "05:00", "closing_time": "22:00",
                "description": "Historic Dravidian masterpiece with 14 soaring gopurams adorned with thousands of colorful mythological stucco sculptures, Golden Lotus tank, and Hall of Thousand Pillars.",
                "best_time_to_visit": "Early Morning / Evening", "difficulty": "Easy"
            },
            {
                "id": "poi_mdu_thirumalai_nayakkar", "name": "Thirumalai Nayakkar Palace, Madurai", "district": "Madurai", "category": "Heritage",
                "tags": ["palace", "nayak", "architecture", "pillars", "light_show"],
                "lat": 9.9150, "lng": 78.1244, "rating": 4.5, "review_count": 32000, "entry_fee_per_person": 30, "typical_duration_minutes": 75,
                "opening_time": "09:00", "closing_time": "17:00",
                "description": "17th-century palace constructed by King Thirumalai Nayak, celebrated for monumental stucco arches, massive cylindrical pillars, and regal courtyard.",
                "best_time_to_visit": "Morning / Evening Light Show", "difficulty": "Easy"
            },
            {
                "id": "poi_mdu_gandhi_museum", "name": "Gandhi Memorial Museum, Madurai", "district": "Madurai", "category": "Heritage",
                "tags": ["gandhi", "freedom_struggle", "museum", "history", "heritage"],
                "lat": 9.9325, "lng": 78.1405, "rating": 4.5, "review_count": 18000, "entry_fee_per_person": 0, "typical_duration_minutes": 60,
                "opening_time": "10:00", "closing_time": "17:45",
                "description": "Housed in the historic Rani Mangammal palace, preserving Mahatma Gandhi's blood-stained dhoti from his 1948 assassination and freedom movement archives.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_mdu_residency", "name": "Madurai Temple View Residency", "district": "Madurai", "category": "Budget Hotel",
                "price_per_night": 1700, "rating": 4.4, "review_count": 1650, "lat": 9.9210, "lng": 78.1180,
                "address": "West Veli Street, Madurai", "amenities": ["Free Wi-Fi", "Air Conditioning", "Rooftop Gopuram View", "24/7 Front Desk"],
                "room_type": "Deluxe Double AC Room", "description": "Comfortable budget hotel situated walking distance from Meenakshi Temple, boasting rooftop vistas of illuminated gopurams."
            }
        ],
        [
            {
                "id": "food_mdu_murugan_idli", "name": "Murugan Idli Shop, Madurai", "district": "Madurai", "category": "Local Food",
                "cuisine": "Traditional Tamil Vegetarian & Tiffin", "specialties": ["Melt-in-mouth Steamed Idlis", "Crispy Ghee Podi Dosa", "Four Chutney Assortment", "Jigarthanda Cooler"],
                "cost_for_two": 260, "rating": 4.8, "review_count": 38000, "lat": 9.9180, "lng": 78.1170, "opening_time": "06:30", "closing_time": "23:00",
                "description": "Legendary Madurai establishment famous across India for cloud-soft idlis slathered with spiced podi and four varieties of fresh coconut chutney."
            },
            {
                "id": "food_mdu_famous_jigarthanda", "name": "Famous Jigarthanda Since 1977, Madurai", "district": "Madurai", "category": "Local Food",
                "cuisine": "Traditional Madurai Coolers", "specialties": ["Special Famous Jigarthanda", "Badam Pisin Nannari Milk", "Basundi Ice Cream"],
                "cost_for_two": 160, "rating": 4.9, "review_count": 42000, "lat": 9.9175, "lng": 78.1185, "opening_time": "09:00", "closing_time": "23:30",
                "description": "The quintessential royal Madurai cooler prepared with pure almond tree gum (badam pisin), nannari root syrup, condensed milk, and clotted cream."
            }
        ]
    )

    # 29. Sivaganga (Chettinad)
    add_district(
        "sivaganga", "Sivaganga", ["sivaganga", "chettinad", "karaikudi"], "Chettinad Heritage", "Sivaganga", 9.8433, 78.4809, False, 102,
        "The opulent land of Chettinad, celebrated for magnificent merchant mansions with Burma teak and Belgian glass, Athangudi handmade tiles, and world-famous Chettinad cuisine.",
        ["Authentic Chettinad Kozhi Varuval", "Kavuni Arisi Sweet (black sticky rice)", "Chettinad Nandu Masala (Crab Curry)", "Vazhaipoo Vadai"],
        [
            {
                "id": "poi_svg_kanadukathan", "name": "Chettinad Merchant Mansions of Kanadukathan", "district": "Sivaganga", "category": "Heritage",
                "tags": ["mansions", "heritage", "chettinad", "burma_teak", "italian_marble"],
                "lat": 10.0710, "lng": 78.7840, "rating": 4.8, "review_count": 28000, "entry_fee_per_person": 50, "typical_duration_minutes": 150,
                "opening_time": "09:00", "closing_time": "17:30",
                "description": "Breathtaking 19th-century palatial residences of Nattukottai Chettiars adorned with carved Burma teak pillars, Athangudi terracotta tiles, and Belgian crystal chandeliers.",
                "best_time_to_visit": "Morning / Late Afternoon", "difficulty": "Easy"
            },
            {
                "id": "poi_svg_athangudi", "name": "Athangudi Handmade Terracotta Tile Studios", "district": "Sivaganga", "category": "Heritage",
                "tags": ["athangudi", "handicrafts", "tiles", "artisan", "heritage"],
                "lat": 10.1550, "lng": 78.7910, "rating": 4.7, "review_count": 12000, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "09:00", "closing_time": "17:00",
                "description": "Artisan village workshops crafting world-famous glazed floor tiles by hand using local soil, colored oxides, and geometric glass stencils.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_svg_chettinad_mansion", "name": "Chettinad Heritage Courtyard Mansion, Kanadukathan", "district": "Sivaganga", "category": "Luxury Resort",
                "price_per_night": 4800, "rating": 4.8, "review_count": 1420, "lat": 10.0710, "lng": 78.7840,
                "address": "Kanadukathan, Sivaganga District", "amenities": ["Burma Teak Pillars", "Swimming Pool", "Chettinad Dining Hall", "Heritage Tour"],
                "room_type": "Royal Heritage Suite", "description": "Authentically restored 19th-century merchant mansion featuring Italian marble, Belgian mirrors, and authentic silver-thali banquets."
            }
        ],
        [
            {
                "id": "food_svg_visalam", "name": "Visalam Authentic Chettinad Kitchen, Kanadukathan", "district": "Sivaganga", "category": "Local Food",
                "cuisine": "Chettinad Spicy Traditional", "specialties": ["Chettinad Kozhi Varuval", "Kavuni Arisi Sweet (Black Rice)", "Nandu Masala (Crab Curry)", "Vazhaipoo Vadai"],
                "cost_for_two": 550, "rating": 4.8, "review_count": 11000, "lat": 10.0730, "lng": 78.7860, "opening_time": "12:00", "closing_time": "22:00",
                "description": "Home-style recipes flavored with roasted peppercorn, kalpasi (stone flower), and star anise served on fresh banana leaves."
            }
        ]
    )

    # 30. Virudhunagar
    add_district(
        "virudhunagar", "Virudhunagar", ["virudhunagar", "srivilliputhur"], "Pandiya South", "Virudhunagar", 9.5680, 77.9624, False, 117,
        "Spiritual land home to the iconic Srivilliputhur Andal Temple (the 11-tier gopuram that forms the official Emblem of Tamil Nadu) and GI-tagged Srivilliputhur Palkova.",
        ["GI-Tagged Srivilliputhur Palkova (sweetened condensed milk)", "Virudhunagar Ennai Parotta", "Ayyanar Falls Herbal Broth"],
        [
            {
                "id": "poi_vrd_srivilliputhur", "name": "Srivilliputhur Andal Temple (Tamil Nadu State Emblem)", "district": "Virudhunagar", "category": "Heritage",
                "tags": ["emblem_of_tamilnadu", "temple", "andal", "gopuram", "heritage", "divya_desam"],
                "lat": 9.5125, "lng": 77.6322, "rating": 4.8, "review_count": 31000, "entry_fee_per_person": 0, "typical_duration_minutes": 105,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "Consecrated in the 8th century, its towering 192-foot 11-tier Raja Gopuram was chosen by the government as the official emblem of Tamil Nadu.",
                "best_time_to_visit": "Early Morning / Evening", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_vrd_heritage", "name": "Srivilliputhur Heritage Residency", "district": "Virudhunagar", "category": "Budget Hotel",
                "price_per_night": 1450, "rating": 4.3, "review_count": 480, "lat": 9.5150, "lng": 77.6350,
                "address": "Madurai Road, Srivilliputhur", "amenities": ["Air Conditioning", "Free Parking", "Veg Restaurant"],
                "room_type": "Standard Deluxe AC", "description": "Comfortable, clean budget hotel located near the historic Andal temple."
            }
        ],
        [
            {
                "id": "food_vrd_palkova", "name": "Sri Venkateswara Palkova Stall & Parotta, Srivilliputhur", "district": "Virudhunagar", "category": "Local Food",
                "cuisine": "Traditional Tamil Sweets & Tiffin", "specialties": ["Authentic GI-Tagged Srivilliputhur Palkova", "Ennai Parotta with Salna", "Halwa"],
                "cost_for_two": 180, "rating": 4.9, "review_count": 26000, "lat": 9.5130, "lng": 77.6330, "opening_time": "07:00", "closing_time": "22:30",
                "description": "World-famous GI-tagged sweet made strictly by slow-simmering pure cow milk with cane sugar over firewood."
            }
        ]
    )

    # 31. Ramanathapuram
    add_district(
        "ramanathapuram", "Ramanathapuram", ["ramanathapuram", "rameswaram", "dhanushkodi"], "Sacred Maritime Coast", "Ramanathapuram", 9.2876, 79.3129, False, 10,
        "Sacred island pilgrimage gateway home to Ramanathaswamy Temple (with the longest pillared corridor in the world), Pamban sea bridge, and Dhanushkodi ghost town at Ram Setu point.",
        ["Rameswaram Fresh Blue Crab Roast", "Coastal Seer Fish Kuzhambu", "Temple Coconut Sweet Pongal"],
        [
            {
                "id": "poi_ram_ramanathaswamy", "name": "Ramanathaswamy Temple & 22 Theerthams, Rameswaram", "district": "Ramanathapuram", "category": "Heritage",
                "tags": ["temple", "jyotirlinga", "corridor", "pamban", "theerthams", "sacred"],
                "lat": 9.2881, "lng": 79.3174, "rating": 4.9, "review_count": 82000, "entry_fee_per_person": 25, "typical_duration_minutes": 180,
                "opening_time": "05:00", "closing_time": "21:00",
                "description": "One of the twelve sacred Jyotirlingas, boasting the longest pillared corridor in the world (1,212 meters) with 1,212 intricately carved sandstone pillars.",
                "best_time_to_visit": "Early Morning (Theertham Baths)", "difficulty": "Easy to Moderate"
            },
            {
                "id": "poi_ram_dhanushkodi", "name": "Dhanushkodi Ghost Town & Ram Setu Point", "district": "Ramanathapuram", "category": "Beaches",
                "tags": ["ghost_town", "ram_setu", "ocean_confluence", "ruins", "beach"],
                "lat": 9.1786, "lng": 79.4167, "rating": 4.8, "review_count": 56000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "06:00", "closing_time": "18:00",
                "description": "Eerie coastal sand spit where the Bay of Bengal meets the Indian Ocean, destroyed in the 1964 cyclone, showing church ruins and Ram Setu land's end.",
                "best_time_to_visit": "Sunrise / Early Morning", "difficulty": "Easy"
            },
            {
                "id": "poi_ram_pamban_bridge", "name": "Pamban Rail & Sea Bridge", "district": "Ramanathapuram", "category": "Heritage",
                "tags": ["bridge", "engineering", "sea", "ocean", "train", "scenic"],
                "lat": 9.2789, "lng": 79.1983, "rating": 4.8, "review_count": 48000, "entry_fee_per_person": 0, "typical_duration_minutes": 60,
                "opening_time": "00:00", "closing_time": "23:59",
                "description": "India's first sea bridge opened in 1914, spanning 2.06 kilometers over the Indian Ocean with a double-leaf bascule section that lifts for ships.",
                "best_time_to_visit": "Sunset / Train Crossing", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_ram_sea_view", "name": "Rameswaram Sea View Residency", "district": "Ramanathapuram", "category": "Budget Hotel",
                "price_per_night": 1400, "rating": 4.3, "review_count": 890, "lat": 9.2850, "lng": 79.3140,
                "address": "Agni Theertham Road, Rameswaram", "amenities": ["Sea Breeze Balcony", "Air Conditioning", "Filtered Water", "Temple Escort"],
                "room_type": "Double Bedded AC Room", "description": "Centrally positioned for coastal theertham baths and morning temple darshans with clean facilities."
            }
        ],
        [
            {
                "id": "food_ram_saravana", "name": "Sri Saravana Veg & Coastal Kitchen, Rameswaram", "district": "Ramanathapuram", "category": "Local Food",
                "cuisine": "Traditional Tamil & Island Cuisine", "specialties": ["Ghee Pongal with Coconut Chutney", "Filter Kaapi", "Island Fresh Crab Roast", "Curd Rice"],
                "cost_for_two": 260, "rating": 4.6, "review_count": 18000, "lat": 10.2870, "lng": 79.3160, "opening_time": "06:00", "closing_time": "22:30",
                "description": "Popular establishment serving clean pilgrim tiffins in the morning and spicy coastal catch curries."
            }
        ]
    )

    # 32. Thoothukudi
    add_district(
        "thoothukudi", "Thoothukudi", ["thoothukudi", "tuticorin", "tiruchendur"], "Pearl City Coast", "Thoothukudi", 8.7642, 78.1348, False, 4,
        "Historic 'Pearl City' of South India, home to the sea-washed Tiruchendur Subramanya Swamy temple, Portuguese Our Lady of Snows Basilica, and famous Tuticorin macaroons.",
        ["GI-Tagged Thoothukudi Cashew Macaroon", "Tuticorin Parotta with Salna", "Karupatti (Palm Jaggery) Halwa"],
        [
            {
                "id": "poi_tho_tiruchendur", "name": "Thiruchendur Subramanya Swamy Temple", "district": "Thoothukudi", "category": "Heritage",
                "tags": ["murugan", "seashore", "padaiveedu", "temple", "coastal"],
                "lat": 8.4965, "lng": 78.1287, "rating": 4.9, "review_count": 68000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "05:00", "closing_time": "21:30",
                "description": "Second Padaiveedu of Lord Murugan, spectacularly located right on the shoreline waves of the Gulf of Mannar with a 137-foot nine-tier gopuram.",
                "best_time_to_visit": "Early Morning / Twilight", "difficulty": "Easy"
            },
            {
                "id": "poi_tho_snows_basilica", "name": "Our Lady of Snows Basilica, Tuticorin", "district": "Thoothukudi", "category": "Heritage",
                "tags": ["church", "basilica", "portuguese", "heritage", "architecture"],
                "lat": 8.8058, "lng": 78.1561, "rating": 4.7, "review_count": 19000, "entry_fee_per_person": 0, "typical_duration_minutes": 60,
                "opening_time": "06:00", "closing_time": "20:00",
                "description": "16th-century Portuguese Roman Catholic church elevated to minor basilica status, enshrining a miraculous statue of Our Lady of Snows brought from Manila in 1555.",
                "best_time_to_visit": "Morning / Evening", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_tho_regency", "name": "Regency Tuticorin by GRT Hotels", "district": "Thoothukudi", "category": "Budget Hotel",
                "price_per_night": 2400, "rating": 4.5, "review_count": 1400, "lat": 8.7980, "lng": 78.1450,
                "address": "Palayamkottai Road, Tuticorin", "amenities": ["Air Conditioning", "Free Wi-Fi", "Restaurant", "Fitness Center"],
                "room_type": "Executive Double Room", "description": "High-quality hotel offering comfortable stays and local coastal gastronomy."
            }
        ],
        [
            {
                "id": "food_tho_macaroon", "name": "Bell Macaroons & Alwar Parotta, Tuticorin", "district": "Thoothukudi", "category": "Local Food",
                "cuisine": "Traditional Pearl City Delicacies", "specialties": ["Authentic Thoothukudi Cashew Macaroon", "Tuticorin Kothu Parotta with Salna", "Karupatti Coffee"],
                "cost_for_two": 220, "rating": 4.9, "review_count": 28000, "lat": 8.8020, "lng": 78.1480, "opening_time": "08:00", "closing_time": "22:30",
                "description": "Legendary confectioners creating airy, melt-in-the-mouth conical macaroons made solely with egg whites, cashew nuts, and sugar."
            }
        ]
    )

    # 33. Tirunelveli
    add_district(
        "tirunelveli", "Tirunelveli", ["tirunelveli", "nellai"], "Thamirabarani River Valley", "Tirunelveli", 8.7139, 77.7567, False, 47,
        "Ancient cultural stronghold on the perennial Thamirabarani river, celebrated for the monumental Nellaiappar Temple (musical pillars), and world-famous Iruttu Kadai Halwa.",
        ["GI-Tagged Tirunelveli Iruttu Kadai Halwa (wheat halwa in pure ghee)", "Sodhi Kuzhambu (coconut milk vegetable stew)", "Thamirabarani Meen Curry"],
        [
            {
                "id": "poi_tnv_nellaiappar", "name": "Nellaiappar Temple & Musical Stone Pillars", "district": "Tirunelveli", "category": "Heritage",
                "tags": ["temple", "shiva", "musical_pillars", "golden_lotus", "heritage"],
                "lat": 8.7281, "lng": 77.6892, "rating": 4.9, "review_count": 46000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "05:30", "closing_time": "21:00",
                "description": "Massive 7th-century temple complex covering 14 acres dedicated to Lord Shiva and Goddess Gandhimathi, famed for cluster pillars that ring musical notes when struck.",
                "best_time_to_visit": "Early Morning / Evening", "difficulty": "Easy"
            },
            {
                "id": "poi_tnv_manimuthar", "name": "Manimuthar Falls & Dam Reserve", "district": "Tirunelveli", "category": "Waterfalls",
                "tags": ["waterfall", "western_ghats", "dam", "forest", "nature"],
                "lat": 8.5833, "lng": 77.4167, "rating": 4.6, "review_count": 21000, "entry_fee_per_person": 25, "typical_duration_minutes": 120,
                "opening_time": "08:00", "closing_time": "17:00",
                "description": "Perennial mountain cascade tumbling into a natural pond at the foot of the Western Ghats tiger reserve.",
                "best_time_to_visit": "Morning", "difficulty": "Easy to Moderate"
            }
        ],
        [
            {
                "id": "hotel_tnv_apple_tree", "name": "Hotel Apple Tree Tirunelveli", "district": "Tirunelveli", "category": "Budget Hotel",
                "price_per_night": 2100, "rating": 4.4, "review_count": 1350, "lat": 8.7180, "lng": 77.7490,
                "address": "North Bypass Road, Tirunelveli", "amenities": ["Air Conditioning", "Free Wi-Fi", "Pure Veg Restaurant", "Travel Desk"],
                "room_type": "Executive AC Room", "description": "Modern hotel located close to the railway junction and Nellaiappar temple."
            }
        ],
        [
            {
                "id": "food_tnv_iruttu_kadai", "name": "Iruttu Kadai Original Halwa Since 1900, Tirunelveli", "district": "Tirunelveli", "category": "Local Food",
                "cuisine": "Traditional Nellai Sweet", "specialties": ["Original Warm Wheat Halwa (served on banaleaf)", "Sodhi Meals Thali", "Koozh with Sundal"],
                "cost_for_two": 160, "rating": 4.9, "review_count": 52000, "lat": 9.7285, "lng": 77.6895, "opening_time": "17:00", "closing_time": "20:30",
                "description": "World-famous modest shop that opens only in the evening with a single bulb, selling warm, melting wheat halwa made with pure ghee and Thamirabarani water."
            }
        ]
    )

    # 34. Tenkasi
    add_district(
        "tenkasi", "Tenkasi", ["tenkasi", "courtallam", "kutralam"], "Western Ghats Waterfalls Valley", "Tenkasi", 8.9594, 77.3161, True, 160,
        "The 'Spa of South India' nestled at the base of the Western Ghats, famed for Courtallam's medicated waterfalls, 180-ft gopuram of Kasi Viswanathar temple, and herbal parotta.",
        ["Courtallam Medicated Herbal Parotta with Country Chicken", "Tenkasi Puttu", "Nannari Sarbath"],
        [
            {
                "id": "poi_tks_courtallam_main", "name": "Courtallam Main Falls & Five Falls ('Spa of South India')", "district": "Tenkasi", "category": "Waterfalls",
                "tags": ["waterfall", "ayurvedic", "spa_of_south_india", "five_falls", "nature", "herbal"],
                "lat": 8.9298, "lng": 77.2694, "rating": 4.7, "review_count": 62000, "entry_fee_per_person": 0, "typical_duration_minutes": 150,
                "opening_time": "05:00", "closing_time": "20:00",
                "description": "Revered natural cascades tumbling through Western Ghats medicinal herbal forests, delivering natural therapeutic baths celebrated in Tamil literature for millennia.",
                "best_time_to_visit": "June to September (Season) / Early Morning", "difficulty": "Easy"
            },
            {
                "id": "poi_tks_kasi_viswanathar", "name": "Kasi Viswanathar Temple, Tenkasi", "district": "Tenkasi", "category": "Heritage",
                "tags": ["temple", "tenkasi", "180ft_gopuram", "heritage", "shiva"],
                "lat": 8.9594, "lng": 77.3161, "rating": 4.8, "review_count": 22000, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "06:00", "closing_time": "20:30",
                "description": "Constructed in 1440 CE by King Parakkirama Pandian ('Kasi of the South'), featuring a 180-foot high nine-tier Rajagopuram that catches gentle mountain breezes.",
                "best_time_to_visit": "Morning / Evening", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_tks_mount_mist", "name": "Mount n Mist Resort Courtallam", "district": "Tenkasi", "category": "Budget Hotel",
                "price_per_night": 1700, "rating": 4.3, "review_count": 760, "lat": 8.9320, "lng": 77.2720,
                "address": "Five Falls Road, Courtallam", "amenities": ["Waterfall View", "Air Conditioning", "Free Parking", "Veg/Non-Veg Restaurant"],
                "room_type": "Deluxe Mountain AC Room", "description": "Comfortable hillside resort offering quick access to Five Falls and herbal streams."
            }
        ],
        [
            {
                "id": "food_tks_border_rahmath", "name": "Border Rahmath Parotta Stall, Tenkasi / Courtallam", "district": "Tenkasi", "category": "Local Food",
                "cuisine": "Traditional Country Non-Veg", "specialties": ["Coin Parotta in Country Ghee", "Pepper Country Chicken Fry", "Salna Gravy", "Garlic Herbal Broth"],
                "cost_for_two": 340, "rating": 4.8, "review_count": 31000, "lat": 8.9580, "lng": 77.3140, "opening_time": "17:00", "closing_time": "23:30",
                "description": "Legendary border food institution serving crispy, feather-light coin parottas soaked in aromatic pepper country chicken gravies."
            }
        ]
    )

    # 35. Kanyakumari
    add_district(
        "kanyakumari", "Kanyakumari", ["kanyakumari", "cape comorin"], "Land's End / Southernmost Cape", "Kanyakumari", 8.0883, 77.5385, False, 10,
        "The majestic southernmost tip of mainland India, where the Indian Ocean, Arabian Sea, and Bay of Bengal converge, home to Vivekananda Rock Memorial and 133-ft Thiruvalluvar Statue.",
        ["Kanyakumari Nanjil Nadu Fish Curry with Tapioca", "Red Banana (Sevvaazhai)", "Crispy Pazha Bajji with Coconut Chutney", "Chukku Kaapi"],
        [
            {
                "id": "poi_kan_vivekananda", "name": "Vivekananda Rock Memorial & 133-Ft Thiruvalluvar Statue", "district": "Kanyakumari", "category": "Heritage",
                "tags": ["monument", "rock_memorial", "thiruvalluvar", "ocean", "ferry", "triveni_sangam"],
                "lat": 8.0781, "lng": 77.5552, "rating": 4.9, "review_count": 95000, "entry_fee_per_person": 50, "typical_duration_minutes": 150,
                "opening_time": "08:00", "closing_time": "16:30",
                "description": "Iconic granite monument erected in 1970 on an offshore rock where Swami Vivekananda meditated in 1892, adjacent to the monumental 133-foot stone statue of saint-poet Thiruvalluvar.",
                "best_time_to_visit": "Morning (Ferry)", "difficulty": "Easy"
            },
            {
                "id": "poi_kan_triveni_sangam", "name": "Triveni Sangam & Sunset / Sunrise Viewpoint", "district": "Kanyakumari", "category": "Beaches",
                "tags": ["sunrise", "sunset", "triveni_sangam", "three_oceans", "land_end"],
                "lat": 8.0772, "lng": 77.5510, "rating": 4.8, "review_count": 78000, "entry_fee_per_person": 0, "typical_duration_minutes": 90,
                "opening_time": "05:00", "closing_time": "21:00",
                "description": "Unique geographic point on Earth where three seas meet, celebrated for watching the sun rise and set over the same ocean waters.",
                "best_time_to_visit": "Sunrise (06:00) / Sunset (18:00)", "difficulty": "Easy"
            },
            {
                "id": "poi_kan_padmanabhapuram", "name": "Padmanabhapuram Wooden Palace (Thuckalay)", "district": "Kanyakumari", "category": "Heritage",
                "tags": ["palace", "wooden_architecture", "travancore", "heritage", "antiquity"],
                "lat": 8.2508, "lng": 77.3278, "rating": 4.8, "review_count": 36000, "entry_fee_per_person": 40, "typical_duration_minutes": 105,
                "opening_time": "09:00", "closing_time": "16:30",
                "description": "Magnificent 16th-century royal palace of the Travancore kings built entirely of teakwood, rosewood, and polished stone at the foot of the Veli Hills.",
                "best_time_to_visit": "Morning", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_kan_sparsa", "name": "Sparsa Resort Kanyakumari", "district": "Kanyakumari", "category": "Budget Hotel",
                "price_per_night": 2800, "rating": 4.6, "review_count": 1800, "lat": 8.0820, "lng": 77.5450,
                "address": "Main Beach Road, Kanyakumari", "amenities": ["Swimming Pool", "Ocean View", "Free Wi-Fi", "Multi-Cuisine Dining"],
                "room_type": "Sea Facing Deluxe Room", "description": "Eco-friendly beachfront resort offering direct views of the sunrise over the three seas."
            }
        ],
        [
            {
                "id": "food_kan_saravana", "name": "Saravana Pure Veg Sunrise Point, Kanyakumari", "district": "Kanyakumari", "category": "Local Food",
                "cuisine": "Nanjil Nadu & South Indian", "specialties": ["Ghee Roast Dosa with Red Chutney", "Nanjil Style Aviyal Meals", "Sweet Pazha Bajji", "Filter Kaapi"],
                "cost_for_two": 240, "rating": 4.6, "review_count": 21000, "lat": 8.0810, "lng": 77.5480, "opening_time": "06:00", "closing_time": "22:30",
                "description": "Premier dining spot for catching the ocean sunrise while enjoying piping hot ghee roast dosas and fresh coconut chutneys."
            }
        ]
    )

    # 36. Nagapattinam
    add_district(
        "nagapattinam", "Nagapattinam", ["nagapattinam", "velankanni", "nagore"], "Coastal Chola Delta", "Nagapattinam", 10.7672, 79.8449, False, 9,
        "Historic multi-faith coastal haven home to the Basilica of Our Lady of Good Health Velankanni, Nagore Dargah shrine, and Point Calimere bird sanctuary.",
        ["Nagore Dum Ka Root Halwa", "Velankanni Fresh Prawn Masala", "Delta Crab Biryani"],
        [
            {
                "id": "poi_nag_velankanni", "name": "Basilica of Our Lady of Good Health, Velankanni", "district": "Nagapattinam", "category": "Heritage",
                "tags": ["church", "basilica", "velankanni", "gothic", "pilgrimage", "beach"],
                "lat": 10.6807, "lng": 79.8496, "rating": 4.8, "review_count": 58000, "entry_fee_per_person": 0, "typical_duration_minutes": 120,
                "opening_time": "05:00", "closing_time": "21:00",
                "description": "Gothic-style Marian minor basilica ('Lourdes of the East') welcoming millions of multi-faith pilgrims on the shores of the Bay of Bengal.",
                "best_time_to_visit": "Morning / Evening", "difficulty": "Easy"
            },
            {
                "id": "poi_nag_nagore_dargah", "name": "Nagore Dargah Shrine (Hazrat Syed Shahul Hameed)", "district": "Nagapattinam", "category": "Heritage",
                "tags": ["dargah", "heritage", "sufi", "minarets", "peace"],
                "lat": 10.8200, "lng": 79.8420, "rating": 4.7, "review_count": 24000, "entry_fee_per_person": 0, "typical_duration_minutes": 75,
                "opening_time": "05:00", "closing_time": "22:00",
                "description": "16th-century Sufi pilgrimage shrine with five minarets, the tallest rising 131 feet, celebrated for communal harmony and evening lamps.",
                "best_time_to_visit": "Evening", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_nag_clinton", "name": "Clinton Park Inn Velankanni", "district": "Nagapattinam", "category": "Budget Hotel",
                "price_per_night": 1700, "rating": 4.3, "review_count": 920, "lat": 10.6820, "lng": 79.8470,
                "address": "Main Road, Velankanni", "amenities": ["Air Conditioning", "Free Wi-Fi", "Restaurant", "Basilica View"],
                "room_type": "Executive Double AC", "description": "Comfortable hotel situated walking distance from the Velankanni basilica shrine."
            }
        ],
        [
            {
                "id": "food_nag_sea_gate", "name": "Hotel Sea Gate Dining Velankanni", "district": "Nagapattinam", "category": "Local Food",
                "cuisine": "Coastal Delta Seafood & South Indian", "specialties": ["Spicy Delta Prawn Roast", "Fried Vanjaram Fish", "Fish Curry Meals", "Nagore Sweet Root"],
                "cost_for_two": 360, "rating": 4.5, "review_count": 12000, "lat": 10.6815, "lng": 79.8480, "opening_time": "11:00", "closing_time": "22:30",
                "description": "Celebrated coastal eatery serving fresh Bay of Bengal fish, prawns, and crabs."
            }
        ]
    )

    # 37. Mayiladuthurai
    add_district(
        "mayiladuthurai", "Mayiladuthurai", ["mayiladuthurai", "tranquebar", "tharangambadi"], "Chola Delta / Cauvery Banks", "Mayiladuthurai", 11.1075, 79.6523, False, 18,
        "Historic cultural epicenter on the Cauvery banks, gateway to the 1620 Danish fort at Tharangambadi (Tranquebar), and ancient Navagraha temples.",
        ["Mayavaram Crispy Ghee Roast", "Tharangambadi Coastal Fish Fry", "Kumbakonam Style Filter Kaapi"],
        [
            {
                "id": "poi_myd_tranquebar", "name": "Fort Dansborg & Danish Heritage Enclave, Tharangambadi", "district": "Mayiladuthurai", "category": "Heritage",
                "tags": ["fort", "danish", "colonial", "tranquebar", "beach", "heritage"],
                "lat": 11.0333, "lng": 79.8542, "rating": 4.7, "review_count": 28000, "entry_fee_per_person": 20, "typical_duration_minutes": 105,
                "opening_time": "09:00", "closing_time": "17:45",
                "description": "Historic Danish fort built in 1620 directly on the ocean shore, featuring Scandinavian bastions, barrel-vaulted governor halls, and maritime museum.",
                "best_time_to_visit": "Morning / Late Afternoon", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_myd_bungalow", "name": "Neemrana's Bungalow on the Beach, Tranquebar", "district": "Mayiladuthurai", "category": "Luxury Resort",
                "price_per_night": 4600, "rating": 4.7, "review_count": 890, "lat": 11.0340, "lng": 79.8550,
                "address": "King Street, Tharangambadi", "amenities": ["Direct Ocean Front", "Swimming Pool", "Danish Heritage Architecture", "Dining Hall"],
                "room_type": "Heritage Sea Facing Room", "description": "Authentically restored 17th-century Danish governor's mansion facing the waves of Fort Dansborg."
            }
        ],
        [
            {
                "id": "food_myd_kaliyakudi", "name": "Kaliyakudi Mess Mayiladuthurai Since 1937", "district": "Mayiladuthurai", "category": "Local Food",
                "cuisine": "Traditional Chola Delta Vegetarian", "specialties": ["Ghee Roast Dosa", "Traditional Plantain Leaf Lunch", "Degre Filter Coffee", "Vadai Sambar"],
                "cost_for_two": 220, "rating": 4.7, "review_count": 14000, "lat": 11.1080, "lng": 79.6540, "opening_time": "06:30", "closing_time": "22:00",
                "description": "Legendary Delta tiffin hall celebrated for hot crispy dosas and rich Cauvery valley vegetable curries."
            }
        ]
    )

    # 38. Tiruvarur
    add_district(
        "tiruvarur", "Tiruvarur", ["tiruvarur", "thiruvarur"], "Chola Delta / Cultural Capital", "Tiruvarur", 10.7725, 79.6365, False, 14,
        "The sacred Carnatic musical capital and birthplace of the musical Trinity (Thyagaraja, Muthuswami Dikshitar & Syama Sastri), famed for Thyagaraja Swamy temple and the colossal Azhi Ther chariot.",
        ["Tiruvarur Azhi Ther Special Ghee Pongal", "Vaduvur Sweet Pongal", "Kumbakonam Kaapi"],
        [
            {
                "id": "poi_tvr_thyagaraja", "name": "Sri Thyagaraja Swamy Temple & Kamalalayam Sacred Tank", "district": "Tiruvarur", "category": "Heritage",
                "tags": ["temple", "chariot", "azhi_ther", "kamalalayam", "carnatic", "heritage"],
                "lat": 10.7767, "lng": 79.6315, "rating": 4.9, "review_count": 32000, "entry_fee_per_person": 0, "typical_duration_minutes": 120,
                "opening_time": "05:30", "closing_time": "21:00",
                "description": "Sprawling 20-acre Chola temple complex fronted by the 33-acre Kamalalayam lake, famed for the world's largest temple chariot (Azhi Ther, 300 tonnes).",
                "best_time_to_visit": "Early Morning / Evening", "difficulty": "Easy"
            }
        ],
        [
            {
                "id": "hotel_tvr_selvies", "name": "Hotel Selvies Tiruvarur", "district": "Tiruvarur", "category": "Budget Hotel",
                "price_per_night": 1500, "rating": 4.3, "review_count": 680, "lat": 10.7740, "lng": 79.6380,
                "address": "Kattur Road, Tiruvarur", "amenities": ["Air Conditioning", "Free Parking", "Veg Restaurant"],
                "room_type": "Executive AC Room", "description": "Comfortable, clean budget hotel walking distance to the historic Thyagaraja temple."
            }
        ],
        [
            {
                "id": "food_tvr_balaji", "name": "Sri Balaji Bhavan Tiruvarur", "district": "Tiruvarur", "category": "Local Food",
                "cuisine": "Traditional Chola Tiffin", "specialties": ["Ghee Pongal with Sambhar", "Rava Dosa", "Filter Coffee"],
                "cost_for_two": 200, "rating": 4.5, "review_count": 6200, "lat": 10.7730, "lng": 79.6370, "opening_time": "06:00", "closing_time": "22:00",
                "description": "Authentic vegetarian tiffin dining hall serving traditional South Indian breakfast and meals."
            }
        ]
    )

    return data

if __name__ == "__main__":
    dataset = create_complete_dataset()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "tamilnadu_complete_seed.json")
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        
    # Also update tamilnadu_seed.json so existing references get full coverage
    tn_legacy_path = os.path.join(data_dir, "tamilnadu_seed.json")
    with open(tn_legacy_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated complete Tamil Nadu dataset!")
    print(f"Districts: {len(dataset['districts'])}")
    print(f"Total POIs: {len(dataset['pois'])}")
    print(f"Total Hotels: {len(dataset['hotels'])}")
    print(f"Total Food Places: {len(dataset['food_places'])}")
    print(f"Ghat Corridors: {len(dataset['ghat_corridors'])}")
    print(f"Saved to: {out_path}")
