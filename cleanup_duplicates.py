import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ============================================================
# 👇👇👇 YOUR FOLDER ID (Make sure this is correct!) 👇👇👇
# ============================================================
GOOGLE_DRIVE_FOLDER_ID = '1J-bAv2meRSuk8HMeELgn0vbiy16IDTee'
# ============================================================

def get_drive_service():
    """Logs into Google and returns the drive service."""
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def main():
    print("🤖 Starting the Clean-up Robot...")
    drive_service = get_drive_service()
    
    files_by_name = {}
    page_token = None
    total_files_scanned = 0

    print(f"🔎 Scanning folder for all files...")

    # We need a loop in case you have more than 100 files
    while True:
        results = drive_service.files().list(
            q=f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false",
            fields="nextPageToken, files(id, name)",
            pageSize=100, # Get 100 files at a time
            pageToken=page_token
        ).execute()
        
        files = results.get('files', [])
        total_files_scanned += len(files)

        # This part groups the files by name
        for file in files:
            file_name = file.get('name')
            file_id = file.get('id')
            
            if file_name not in files_by_name:
                files_by_name[file_name] = [] # Create a new list for this name
            
            files_by_name[file_name].append(file_id) # Add the file ID

        # Check if there is another page of files
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break # No more pages, exit the loop

    print(f"✅ Scan complete. Found {total_files_scanned} files in total.")
    
    total_deleted = 0
    # Now, loop through our grouped list and find duplicates
    for name, ids in files_by_name.items():
        if len(ids) > 1:
            print(f"  Found duplicates for: {name} ({len(ids)} copies)")
            
            # Keep the first file
            ids_to_keep = ids.pop(0) 
            print(f"    ...Keeping file ID: {ids_to_keep}")
            
            # Delete all the rest
            for id_to_delete in ids:
                try:
                    drive_service.files().delete(fileId=id_to_delete).execute()
                    print(f"    ...🗑️ Deleted file ID: {id_to_delete}")
                    total_deleted += 1
                except Exception as e:
                    print(f"    ...❌ FAILED to delete {id_to_delete}: {e}")

    print(f"\n🎉 Clean-up complete! Deleted {total_deleted} duplicate files.")

if __name__ == '__main__':
    main()
    