# Prerequites (for testing manually)
- ensure docker desktop software is running on your computer
- run "docker run -d --hostname esd-rabbit --name rabbitmq-mgmt -p 5672:5672 -p 15672:15672" command
- run "python amqp_setup.py" command (amqp_setup.py is in the amqp folder from root, cd into the folder first before running the command)
- run "python notificationServer.py" command (notificationServer.py is in the Notification folder, cd into the folder first before running the command)
- run "python logServer.py" command (logServer.py is in the Log folder, cd into the folder first before running the command)

## Log server
- consumes messages from the `log_queue` queue with `log.*` routing key and calls the [POST] Add log route to insert into db
- `message format`
```json
{
  "userId": <userId>,
  "subGroupId": <subGroupId>,
  "taskId": <taskId>,
  "type": <type>,
  "description": <description>
}
```

## Notification server
- consumes messages from the `email_queue` queue with `email.*` routing key and sends email
- `message format`
```json
{
  "recipient": <email>,
  "subject": <email_subject>,
  "body": <email_message>
}
```

# API Documentation
Base url: https://personal-rc7vnnm9.outsystemscloud.com

## List of simple miroservices
- User          /UserAPI_REST/rest/v1
- Group         /GroupAPI_REST/rest/v1
- SubGroup      /SubGroupAPI_REST/rest/v1
- Task          /TaskAPI_REST/rest/v1
- Log           /LogAPI_REST/rest/v1
- Document      /DocAPI_REST/rest/v1
- Comment       /CommentAPI_REST/rest/v1

## Authentication
- Each simple microservice API has its own authentication headers to be included
  - User
    - `Headers`
    - "X-User-AppId" = [userAppId]
    - "X-User-Key" = [userAPIKey]
  - Group
    - `Headers`
    - "X-Group-AppId" = [groupAppId]
    - "X-Group-Key" = [groupAPIKey]
  - SubGroup
    - `Headers`
    - "X-SubGroup-AppId" = [subGroupAppId]
    - "X-SubGroup-Key" = [subGroupAPIKey]
  - Task
    - `Headers`
    - "X-Task-AppId" = [taskAppId]
    - "X-Task-Key" = [taskAPIKey]
  - Log
    - `Headers`
    - "X-Log-AppId" = [logAppId]
    - "X-Log-Key" = [logAPIKey]
  - Document
    - `Headers`
    - "X-Doc-AppId" = [docAppId]
    - "X-Doc-Key" = [docAPIKey]
  - Document
    - `Headers`
    - "X-Comment-AppId" = [commentAppId]
    - "X-Comment-Key" = [commentAPIKey]

## Endpoints
- User (https://personal-rc7vnnm9.outsystemscloud.com/UserAPI_REST/rest/v1/)
  - [POST]    Login
    - /login
  - [GET] 		Get all users		
    - /user
  - [GET]		Get a user		
    - /user/{userId}
  - [POST] 		Add user			
    - /user
  - [PUT] 		Update user		
    - /user/{userId}
  - [DELETE] 	Delete user		
    - /user/{userId}
- Group (https://personal-rc7vnnm9.outsystemscloud.com/GroupAPI_REST/rest/v1/)
  - [GET] 		Get all groups			
    - /group
  - [GET]		Get a group			
    - /group/{groupId}
  - [GET]		Get user's groups		
    - /group/usergroup/{userId}
  - [POST] 		Add group			
    - /group
  - [PUT] 		Update group			
    - /group/{groupId}
  - [PUT]		Assign users to group	
    - /group/assign/{groupId}
  - [DELETE] 	Delete group			
    - /group/{groupId}
- SubGroup (https://personal-rc7vnnm9.outsystemscloud.com/SubGroupAPI_REST/rest/v1/)
  - [GET] 		Get all subgroups			
    - /subgroup
  - [GET]		Get a subgroup			
    - /subgroup/{subGroupId}
  - [GET]		Get user's subgroups		
    - /subgroup/usersubgroup/{userId}
  - [GET]		Get group's subgroups		
    - /subgroup/groupsubgroup/{groupId}
  - [POST] 		Add subgroup				
    - /subgroup
  - [PUT] 		Update subgroup			
    - /subgroup/{subGroupId}
  - [PUT]		Self-Enrol user to subgroup	
    - /subgroup/enrol/{subGroupId}/{userId}
  - [DELETE] 	Delete subgroup			
    - /subgroup/{subGroupId}
- Task (https://personal-rc7vnnm9.outsystemscloud.com/TaskAPI_REST/rest/v1/)
  - [GET] 		Get all tasks			
    - /task
  - [GET]		Get all tasks in subgroup 
    - /task/subgroup/{subGroupId}
  - [GET] Get user's tasks
    - /task/usertask/{userId}
  - [GET] Get user's tasks by status
    - /task/usertaskstatus/{userId}
  - [GET] Get task by status
    - /task/status/{status}
  - [POST] 		Add task				
    - /task
  - [PUT] 		Update task			
    - /task/{taskId}
  - [PUT]		Assign task to user		
    - /task/assign
  - [DELETE] 	Delete task			
    - /task/{taskId}
- Log (https://personal-rc7vnnm9.outsystemscloud.com/LogAPI_REST/rest/v1/)
  - [GET] 		Get all logs			
    - /log
  - [GET]		Get a log 
    - /log/{logId}
  - [GET]		Get logs by type		
    - /log/{type}
  - [GET]		Get logs by taskId		
    - /log/taskId/{taskId}
  - [GET]		Get logs by subGroupId	
    - /log/subgroupId/{subGroupId}
  - [POST] 		Add log				
    - /log
  - [PUT] 		Update log			
    - /log/{logId}
  - [DELETE] 	Delete log			
    - /log/{logId}
- Document (https://personal-rc7vnnm9.outsystemscloud.com/DocAPI_REST/rest/v1/)
  - [GET] 		Get document				
    - /doc/{docId}
  - [GET]		Get all document in subgroup 
    - /doc/{subGroupId}
  - [POST] 		Add document		        	
    - /doc/{type}
  - [PUT] 		Update document	        	
    - /doc/{docId}
  - [DELETE] 	Delete document 			
    - /doc/{taskId}
- Comment (https://personal-rc7vnnm9.outsystemscloud.com/CommentAPI_REST/rest/v1/)
  - [GET] 		Get all comments			
    - /comment
  - [GET]		Get all comments in taskId 	
    - /comment/taskId/{taskId}
  - [POST] 		Add comment				
    - /comment
  - [PUT] 		Update comment			
    - /comment/{commentId}
  - [DELETE] 	Delete comment			
    - /comment/{commentId}

## Database schema
- User
  - `User table`
  - [PK] userId (bigint) (auto increment)
  - username (varchar)
  - email (varchar)
  - phone (varchar)
  - password (varchar)
  - role (varchar)
  - picture (binary data)
- Group
  - `Group table`
  - [PK] groupId (bigint) (auto increment)
  - name (varchar)
  - description (varchar)
  - picture (binary data)
  - size (integer)
  - createdDateTime (datetime)
  - `GroupUser table`
  - [FK] groupId (bigint)
  - [FK] userId (bigint)
  - username (varchar)
- SubGroup
  - `SubGroup table`
  - [PK] subGroupId (bigint) (auto increment)
  - [FK] groupId (bigint)
  - name (varchar)
  - description (varchar)
  - picture (binary data)
  - size (int)
  - `SubGroupUser table`
  - [FK] subGroupId (bigint)
  - [FK] userId (bigint)
  - username (varchar)
- Task
  - `Task table`
  - [PK] taskId (bigint) (auto increment)
  - name (varchar)
  - description (varchar)
  - [FK] createdById (bigint)
  - createdByUsername (varchar)
  - [FK] subGroupId (bigint)
  - subGroupName (varchar)
  - createdDateTime (datetime)
  - [FK] assignorUserId (bigint)
  - assignorUsername (varchar)
  - lastUpdatedDateTime (datetime)
  - [FK] lastUpdatedById (bigint)
  - lastUpdatedByUsername (varchar)
  - dueDateTime (datetime)
  - status (varchar)
  - `TaskAssignment`
  - [FK] taskId (bigint)
  - [FK] assigneeUserId (bigint)
  - assigneeUsername (varchar)
- Log
  - `Log table`
  - [PK] LogId (bigint) (auto increment)
  - [FK] userId (bigint)
  - type (varchar)
  - [FK] taskId (bigint)
  - [FK] subGroupId (bigint)
  - description (varchar)
  - timestamp (datetime)
- Document
  - `Document table`
  - [PK] DocId (bigint) (auto increment)
  - [FK] subGroupId (bigint)
  - document (binary data)
- Comment
  - `Comment table`
  - [PK] commentId (bigint) (auto increment)
  - [FK] taskId (bigint)
  - [FK] userId (bigint)
  - username (varchar)
  - createdDateTime (datetime)
  - comment (varchar)
  - picture (binary data)