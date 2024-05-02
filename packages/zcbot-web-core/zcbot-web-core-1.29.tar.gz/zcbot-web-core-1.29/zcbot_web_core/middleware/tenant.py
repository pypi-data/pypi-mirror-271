# from starlette.requests import Request
# from starlette.responses import Response
# from starlette.middleware.base import BaseHTTPMiddleware
# from ..auth.share_auth import ShareAuth
# from ..context.context_vars import auth_user_context, tenant_context
# from ..lib import logger
#
# LOGGER = logger.get('租户中间件')
# share_auth = ShareAuth()
#
#
# class TenantMiddleware(BaseHTTPMiddleware):
#     """ 租户中间件 """
#
#     def __init__(self, app):
#         super().__init__(app)
#
#     async def dispatch(self, request: Request, next_func) -> Response:
#         """
#         租户挂载中间件
#         :param request:
#         :param next_func:
#         :return:
#         """
#         # 挂载
#         auth_user = share_auth.get_auth_user(request)
#         auth_user_context.set(auth_user)
#         if auth_user and auth_user.tenantCode:
#             # 复用auth_user避免重复解析用户
#             tenant_context.set(auth_user.tenantCode)
#         # 执行
#         response = await next_func(request)
#         # 清理
#         tenant_context.set(None)
#         auth_user_context.set(None)
#
#         return response
