# THIS COMMAND HAS BEEN DEPRECATED AND CAN NOW BE DONE VIA THE ADMIN PANEL#

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

ORG_SETTINGS_URL = "https://app.snyk.io/admin/org/{}"

def wait_for_pageload(driver):
    WebDriverWait(driver, timeout=120).until(
        EC.presence_of_element_located((By.CLASS_NAME, "header__title"))
    )

def unset_ff_in_org(driver, org_id, target_ff):
    # First go to the settings page for our org
    driver.get(ORG_SETTINGS_URL.format(org_id))
    wait_for_pageload(driver)

    # Next we'll select the delect checkbox for our ff
    delete_checkbox = driver.find_element(By.NAME, f"delete-{target_ff}")
    delete_checkbox.click()

    # Now we have to click the update button
    delete_checkbox.submit()
    wait_for_pageload(driver)


def set_ff_in_org(driver, org_id, target_ff):
    # First go to the settings page for our org
    driver.get(ORG_SETTINGS_URL.format(org_id))
    wait_for_pageload(driver)

    # Next, let's select our feature flag
    select = Select(driver.find_element(By.NAME, "newName"))
    select.select_by_value(target_ff)

    # Now enter a value
    input_text = driver.find_element(By.NAME, "newValue")
    input_text.clear()
    input_text.send_keys("false")

    # Now we have to click the update button
    input_text.submit()
    wait_for_pageload(driver)

def setFeatureFlag(driver, orgIds, featureFlagName, unset):
    for org in orgIds:
        try:
            if unset:
                unset_ff_in_org(driver, org, featureFlagName)
            else:
                set_ff_in_org(driver, org, featureFlagName)
        except:
            print(f"Error: Unable to set feature flag {featureFlagName} in org {org} (unset={unset})")