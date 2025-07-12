
# Random values for timeline post
NAME="TestUser$RANDOM"
EMAIL="testuser$RANDOM@example.com"
CONTENT="This is a test post content $RANDOM"

# POST a new timeline post
echo "Creating a new timeline post..."
POST_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/timeline_post \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$NAME\", \"email\":\"$EMAIL\", \"content\":\"$CONTENT\"}")

echo "POST response:"
echo $POST_RESPONSE

POST_ID=$(echo $POST_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

# GET all timeline posts and check if our post exists
echo "Getting all timeline posts..."
GET_RESPONSE=$(curl -s http://127.0.0.1:5000/api/timeline_post)

echo "GET response:"
echo $GET_RESPONSE

echo "Checking if the created post exists in GET response..."
echo $GET_RESPONSE | grep -q "$CONTENT"
if [ $? -eq 0 ]; then
  echo "Success: Timeline post found!"
else
  echo "Error: Timeline post NOT found."
fi

# Bonus: DELETE the created timeline post
echo "Deleting the created timeline post with id $POST_ID..."
DELETE_RESPONSE=$(curl -s -X DELETE http://127.0.0.1:5000/api/timeline_post/$POST_ID)
echo "DELETE response:"
echo $DELETE_RESPONSE