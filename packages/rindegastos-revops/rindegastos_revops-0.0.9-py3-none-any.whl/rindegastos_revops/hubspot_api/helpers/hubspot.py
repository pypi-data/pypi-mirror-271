from enum import Enum

class Endpoints(Enum):
    """
    ### Endpoints Objetos
    Endpoints para extracción de registros de Objetos en Hubspot ver siguiente URL 
    [View a model of your CRM object and activity relationships](https://knowledge.hubspot.com/data-management/view-a-model-of-your-crm-object-and-activity-relationships)

    #### Objetos del CRM
    * Contacts
    * Companies
    * Tickets

    ### Objetos de Personalizados
    * Holdings (No requerido)
    
    ### Objetos de Ventas
    * Cotizaciones (No requerido)
    * Elementos de Pedido (No requerido)
    * Leads [No disponible mediante API](https://community.hubspot.com/t5/APIs-Integrations/Leads-Object-API/m-p/955434#M72538)
    * Deals

    ### Actividades
    * Postal mail (No requerido)
    * Emails
    * Linkedin Messages (No requerido)
    * Calls
    * Notas (No implementado)
    * Meetings
    * SMS (No requerido)
    * Tasks
    * WhatsApp Messages (No requerido)
    """

    ### Objetos del CRM ###
    # Contacts
    CONTACTS_SEARCH = "objects/contacts/search"
    # Companies
    COMPANIES_SEARCH = "objects/companies/search"
    # Tickets
    TICKETS_SEARCH = "objects/tickets/search"

    ### Objetos de Ventas ###
    # Deals
    DEALS_SEARCH = "objects/deals/search"

    ### Actividades ###
    # Calls
    CALLS_SEARCH = "objects/calls/search"
    # Tasks
    TASKS_SEARCH = "objects/tasks/search"
    # Emails
    EMAILS_SEARCH = "objects/emails/search"
    # Meetings
    MEETINGS_SEARCH = "objects/meetings/search"
    # Notes
    NOTES_SEARCH = "objects/notes/search"

    # Users
    USERS_ALL = "objects/users"

    # Extraer Propiedades de los Objetos
    PROPERTIES_CONTACTS_READ_ALL = "properties/contacts"
    PROPERTIES_COMPANIES_READ_ALL = "properties/companies"
    PROPERTIES_TICKETS_READ_ALL = "properties/tickets"

    PROPERTIES_DEALS_READ_ALL = "properties/deals"

    PROPERTIES_CALLS_READ_ALL = "properties/calls"
    PROPERTIES_TASKS_READ_ALL = "properties/tasks"
    PROPERTIES_EMAILS_READ_ALL = "properties/emails"
    PROPERTIES_MEETINGS_READ_ALL = "properties/meetings"
    PROPERTIES_NOTES_READ_ALL = "properties/notes"

    PROPERTIES_USERS_READ_ALL = "properties/users"




class HubspotConnectorApi:
    def __init__(self, hubspot_api_key):
        self.base_url = "https://api.hubapi.com/crm/v3"

        self.headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': f"Bearer {hubspot_api_key}"
        }
    def endpoint(self, endpoint:Endpoints):
        return f"{self.base_url}/{endpoint.value}"
