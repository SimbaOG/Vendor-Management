REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('accounts.auth.authentication.UserAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('accounts.permissions.auth_permissions.IsAuthenticated',),
}
