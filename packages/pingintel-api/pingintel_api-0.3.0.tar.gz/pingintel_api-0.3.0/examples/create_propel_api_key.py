from propelauth_py import init_base_auth

auth = init_base_auth(
    f"https://auth.staging.pingintel.com",
    "a06629b3f9cc32415fb75997024bdeba4e5d58e05f56da049af9aa97241867e38ca7b946067b688a1ed004548fb1ad82",
)
res = auth.fetch_users_by_query(
    email_or_username="scott",
    include_orgs=False,
)

assert res["total_users"] == 1, res
user = res["users"][0]
# breakpoint()
# res = auth.create_api_key(
#     # org_id="1189c444-8a2d-4c41-8b4b-ae43ce79a492",
#     user_id=user["user_id"],
#     # expires_at_seconds=1630425600,
#     metadata={
#         "customKey": "customValue",
#     },
# )

# print(res{'api_key_id'])
# print(res{'api_key_token'])


res = auth.create_access_token(user_id=user["user_id"], duration_in_minutes=60)
print(res)
