"""Provides a more Pythonic interface to the Nutshell CRM API.

This package provides the NutshellAPI class, and modules for entities, methods, and responses. Naming of classes and
objects is consistent with python conventions for case and naming.

The entities module provides classes for the various entities in the Nutshell CRM system, such as User, Team,
ActivityType, etc.

The methods module provides classes for the JSON-RPC API methods, such as FindUsers, GetUser, GetAnalyticsReport, etc.

The responses module provides classes for the various API responses, such as FindUsersResult, GetUserResult,
GetAnalyticsReportResult, etc.

"""

from .nutshell_api import NutshellAPI
