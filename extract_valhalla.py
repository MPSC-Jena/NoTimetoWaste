import zipfile
import shutil
import os

def main():
    # Paths relative to the root directory
    zip_path = os.path.join('Challenge No Time To Waste', 'Daten', 'valhalla.zip')
    target_dir = os.path.join('backend', 'valhalla_data')

    if not os.path.exists(zip_path):
        print(f"Error: Could not find {zip_path}")
        print("Please ensure you are running this script from the root project directory.")
        return

    # Clean directory if it exists
    if os.path.exists(target_dir):
        print(f"Cleaning {target_dir}...")
        shutil.rmtree(target_dir)

    os.makedirs(target_dir, exist_ok=True)

    # Extract
    print(f"Extracting {zip_path} to {target_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        
    print("Extraction complete.")
    print("\nNext steps to start Valhalla:")
    print("1. cd backend/valhalla_data/valhalla")
    print("2. make dev-up (or: docker-compose -f docker-compose.dev.yml up -d)")

if __name__ == "__main__":
    main()
