import requests
import base64

def get_access_token(client_id, client_secret):
    try:
        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

        if response.status_code != 200:
            return None, f"Error: {response.status_code} - {response.text}"

        access_token = response.json()["access_token"]
        return access_token, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_song_titles(album_link, client_id, client_secret):
    access_token, error = get_access_token(client_id, client_secret)
    if error:
        return None, error

    return get_song_titles_with_token(album_link, access_token)

def get_song_titles_with_token(album_link, access_token):
    try:
        # Extract the album ID from the album link
        album_id = album_link.split('/')[-1]

        # Set up the headers for the API request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Make the API request to get the album details
        response = requests.get(f"https://api.spotify.com/v1/albums/{album_id}/tracks", headers=headers)

        # Check if the request was successful
        if response.status_code != 200:
            return None, f"Error: {response.status_code} - {response.text}"

        # Extract the song titles from the response
        song_titles = [track["name"] for track in response.json()["items"]]

        return song_titles, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# Usage example
client_id = "b26cd1dd777f43379cfc6376ab545246"
client_secret = "43cb24fbef5c4b15a70334df4a4b1747"
album_link = "https://open.spotify.com/album/3t0h9Jw2lbQFCrBuDUMARd"
song_titles, error = get_song_titles(album_link, client_id, client_secret)

if song_titles:
    print("Song titles:", song_titles)
else:
    print("Error:", error)
