=====================================================================================
# global convention
=====================================================================================
## request and response
json

=====================================================================================
# specific convention
=====================================================================================
# register
## route
/api/register
## method
post
## request
{
    username: "new username"
}
## response
### successful
{
    userid: "id"
}
### error
{
    error: "the username cannot be register"
}
=======================================================================================
# login
## route
/api/login
## method
post
## request
{
    username: "text"
}
## response
### successful
{
    userid: "id"
}
### error
{
    error: "user cannot recognized"
}
=====================================================================================
# load guideline
## route
/api/guideline
## method
get
## request
{
    userid: "id",
    path: "guideline path"
}
## response
### successful
{
    guideline: "text"
}
### error
{
    error: "the guideline cannot be loaded"
}
=====================================================================================
# update model following instruction text
## route
/api/instruction
## method
post
## request
{
    userid: "id",
    list_instruction: "list of instruction seperate by newline"
}
## response
### successful
{
    instructions:[
        0:{
            x: "x"
            y: "y"
        }
        1:{
            x: "x"
            y: "y"
        }
        ...
    ]
}
### error
{
    error: "there are something wrong in instruction list"
}