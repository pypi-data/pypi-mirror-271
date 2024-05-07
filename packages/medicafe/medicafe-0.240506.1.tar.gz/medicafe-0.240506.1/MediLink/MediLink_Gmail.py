"""
NOTE: Also download the surgery schedule. So sometimes it doesn't need the OTP.

This script facilitates the process of accessing a notification email from Outlook 365, which contains a secure link to view a message. The script automates the retrieval of this link and the OTP sent by email to authenticate and access the content securely.

**Challenges:**
1. Extracting a 'Read the message' link from an email notification sent via Outlook 365.
2. Monitoring Gmail programmatically for an OTP email sent as part of Microsoft's secure email authentication process.
3. Using the OTP to authenticate and access the secured email content.
4. Securely downloading an attachment (e.g., Carol's CSV with PHI data) directly from Microsoft's servers to the client machine without it ever passing through Google's servers.
5. Handling potential errors and edge cases, such as delays in receiving the OTP email or issues with the link extraction.
6. Ensuring HIPAA compliance in handling PHI data, especially during data transfer directly from Microsoft's secured environment.

**Suggested Approach:**
1. **Authentication and Accessing Gmail**: Use the Gmail API in a client-side Python script to monitor and extract necessary details (links and OTPs) from emails.
2. **Extracting the 'Read the Message' Link**: Identify and extract the URL from the notification email which navigates to Microsoft's secure email portal.
3. **Monitoring for the OTP**: Continuously check the Gmail inbox for an incoming OTP email following the initiation of the authentication process through the extracted link.
4. **Using the OTP**: Use the OTP to complete the authentication process on the Microsoft portal and gain access to the secure content.
5. **Downloading the Attachment**: Once authenticated, directly download the PHI-containing document from the Microsoft portal to the client machine, ensuring encryption and security throughout the transfer process.

**Steps Involved:**
1. Set up the Python client to monitor Gmail and interact with the Google Apps Script for initial link extraction.
2. Extract the 'Read the message' link from the relevant email using the Google Apps Script.
3. Use the Python client to handle user interactions required to navigate the Microsoft authentication portal, enter the OTP, and download the secured content.
4. Ensure secure handling of all PHI data, with strong emphasis on HIPAA compliance throughout the process.

**Breakdown:**

**Python Script (Client Side)**
- **Functionality**:
    - Interface with the user to initiate the process.
    - Monitor Gmail for emails that contain the secure link and OTP.
    - Handle the navigation to the secure Microsoft portal and input the OTP.
    - Directly download the secure content once access is granted.
- **Libraries and APIs**:
    - Google API Python Client to interact with Gmail.
    - Requests for HTTP requests to handle link extraction and OTP monitoring.
    - OS and Sys libraries for local system interactions.

**Google Apps Script (Server Side)**
- **Functionality**:
    - Authenticate and access Gmail to extract the 'Read the message' link.
    - Provide support for initial email filtering and link extraction.
    - Not involved in the decryption or direct handling of PHI data to ensure compliance with HIPAA.

This architecture ensures the system handles sensitive PHI data in compliance with HIPAA regulations while maintaining robust and reliable email processing and file handling mechanisms. All sensitive data transfers occur directly from Microsoft's secure environment, minimizing the risk of unauthorized access during transit.
"""
import requests
import webbrowser
import time
from MediLink_ConfigLoader import log

def initiate_process():
    """
    Initiates the process to retrieve the link and OTP from the Google Apps Script,
    authenticate on Microsoft's secure email portal, and download the secured content.
    """
    log("Process initiated by the user.")
    
    # Retrieve the 'Read the message' link
    link = retrieve_link()
    if link:
        log("Link retrieved: " + link)
        webbrowser.open(link)
        log("Please authenticate and ensure the OTP is received.")
        
        # Poll for the OTP rather than starting a server
        otp = poll_for_otp()
        if otp:
            log("OTP retrieved: " + otp)
            log("Complete the authentication in the opened web browser manually using the retrieved OTP.")
            input("Press Enter after you have completed the download of the file...")
        else:
            log("Failed to retrieve OTP.")
    else:
        log("Failed to retrieve the link.")

def retrieve_link():
    """
    Retrieves the 'Read the message' link from the Google Apps Script.
    """
    try:
        url = "https://script.google.com/macros/s/AKfycbzlq8d32mDlLdtFxgL_zvLJernlGPB64ftyxyH8F1nNlr3P-VBH6Yd0NGa1pbBc5AozvQ/exec"
        params = {'action': 'get_link'}
        response = requests.get(url, params=params)
        if response.status_code == 200 and response.text.startswith("http"):
            return response.text
        else:
            log("Failed to retrieve link: HTTP status {}, Response text: {}".format(response.status_code, response.text))
            return None
    except Exception as e:
        log("Error retrieving link: {}".format(str(e)))
        return None

def poll_for_otp():
    """
    Polls the Google Apps Script for the OTP, waiting until it is available.
    """
    url = "https://script.google.com/macros/s/AKfycbzlq8d32mDlLdtFxgL_zvLJernlGPB64ftyxyH8F1nNlr3P-VBH6Yd0NGa1pbBc5AozvQ/exec"
    params = {'action': 'get_otp'}
    timeout = time.time() + 60*3  # Poll for 3 minutes max
    while time.time() < timeout:
        response = requests.get(url, params=params)
        if response.status_code == 200 and response.text.isdigit():
            return response.text
        elif response.status_code != 200:
            log("Failed to retrieve OTP, HTTP status: {}".format(response.status_code))
        time.sleep(5)  # Poll every 5 seconds
    log("OTP not retrieved within the timeout period.")
    return None

if __name__ == "__main__":
    initiate_process()