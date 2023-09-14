import logging
import sys

from simple_salesforce import Salesforce

from utils import salesforce_login as login

logging.basicConfig(format="%(asctime)s : %(message)s", level=logging.INFO)

#
# sf_credentials = (
#    "<instance_url>",
#    "<session_id>",
# )
#
sf_credentials = (
    "fun-agility-2512-dev-ed.scratch.my.salesforce.com",
    "00D0C0000001unI!ARMAQBJjbcHZjnNG2GH.zHt4lDusCiR6pYdPcWgaX_W.x8Qpv.QScAjLIY4yLdVIkX.Bit_cW8jvo65rKvSF7PJr0EUbXR4g",
)


def build_gloabl_value_set(sf: Salesforce, set_name: str, custom_values: list):
    """build_gloabl_value_set(sf: Salesforce, custom_values: ist)

    Args:
        sf (Salesforce): simple_salesforce Salesforce Client
        set_name (str): name of the global value set
        custom_values (list): picklist values
    """

    values = []
    for custom_value in custom_values:
        values.append(
            sf.mdapi.CustomValue(
                fullName=custom_value,
                default=False,
                label=custom_value,
            )
        )

    global_value_set = sf.mdapi.GlobalValueSet(
        fullName=set_name,
        customValue=values,
        masterLabel=set_name,
        sorted=False,
    )

    return global_value_set


def create_gloabl_value_set(sf: Salesforce, set_name: str, custom_values: list):
    """create_gloabl_value_set(sf: Salesforce, custom_values: ist)

    Args:
        sf (Salesforce): simple_salesforce Salesforce Client
        set_name (str): name of the global value set
        custom_values (list): picklist values
    """

    meta_values = build_gloabl_value_set(sf, set_name, custom_values)
    sf.mdapi.GlobalValueSet.create(meta_values)


def build_custom_field(
    sf: Salesforce, object_name: str, custom_field_name: str, type: str
):
    """build_custom_field(sf: Salesforce, object_name: str, custom_field_name: str, type: str)

    Args:
        sf (Salesforce): simple_salesforce Salesforce Client
        object_name (str): name of the sObject
        custom_field_name (str): name of the custom field
        type (str): type of the custom field
    """

    custom_field = sf.mdapi.CustomField(
        fullName=f"{object_name}.{custom_field_name}__c",
        description=f"{custom_field_name}",
        label=f"{custom_field_name}",
        type=sf.mdapi.FieldType(f"{type}"),
    )

    return custom_field


def create_leaver_category(sf: Salesforce, object_name: str):
    """create_leaver_category(sf: Salesforce, object_name: str)

    Args:
        sf (Salesforce): simple_salesforce Salesforce Client
        object_name (str): name of the sObject
    """

    meta_field = build_custom_field(sf, object_name, "Leaver_Category", "Picklist")
    meta_field.valueSet = sf.mdapi.ValueSet(
        valueSetName="Leaver_Category",
    )
    sf.mdapi.CustomField.create(meta_field)


def delete_custom_field(sf: Salesforce, object_name: str, custom_field_name: str):
    """delete_custom_field(sf: Salesforce, object_name: str)

    Args:
        sf (Salesforce): simple_salesforce Salesforce Client
        object_name (str): name of the sObject
    """
    sf.mdapi.CustomField.delete(f"{object_name}.{custom_field_name}__c")


def update_object(sf: Salesforce):
    """update_object(sf: Salesforce)

    Args:
        sf (Salesforce): simple_salesforce Salesforce Client
    """

    create_gloabl_value_set(sf, "Leaver_Category", ["Leaver", "Mover", "Stayer"])

    create_leaver_category(sf, "Account")
    # delete_custom_field(sf, "Account", "Leaver_Category")


if __name__ == "__main__":
    sf = login(sf_credentials)

    if not sf:
        print("\n*** Not Logged into Salesforce ***\n")
        sys.exit(1)

    print("\n*** Logged into Salesforce ***\n")

    update_object(sf)
