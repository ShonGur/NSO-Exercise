# NSO Exercise
 Home exercise for NSO group

 Created server and tests using Flask framework along with pytest. All messages on the server stored in SQL using sqlite3. Server supports Adding, Fetching and Deleting messages with the following JSON format:
 ```
application_id: {application id}
session_id: {unique session id}
message_id: {unique message id}
participants: [list of participant names]
content: {message}
```
But is easily expandable. 
