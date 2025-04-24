
Step 1. Browser: go to "https://www.dropbox.com/oauth2/authorize?client_id=$DROPBOX_APP_KEY&token_access_type=offline&response_type=code"
Step 2. Copy the access code from the URL
Step 3. Run the following command to get the refresh token
```
curl --location --request POST "https://api.dropboxapi.com/oauth2/token" \
-u "$DROPBOX_APP_KEY:$DROPBOX_APP_SECRET" \
-H "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "code=$DROPBOX_ACCESS_CODE" \
--data-urlencode "grant_type=authorization_code"
```
Step 4. Copy the refresh token from the response
