# Friday Sermon Summary Reminder

This script was created to help me stay on track with my goal of listening to weekly Friday sermons. It automates the process of summarizing and sharing the sermon content. Here's how it works:

## Features

1. **Web Scraping**: The script scrapes the content of the latest Friday sermon summary from a specified URL.

2. **Text-to-Speech Conversion**: It converts the extracted text into an audio file using the `pyttsx3` library.

3. **Google Drive Integration**: The script uploads the audio file to Google Drive using the Google Drive API, making it accessible from anywhere.

4. **Email Notification**: It sends an email containing the shareable link to access the sermon summary, ensuring you never miss an update.

## How to Use

To use this script, follow these steps:

1. **Configuration**:
   - Set up your Google Drive API credentials and save them securely. 
   - Ensure you have the required Python libraries installed, such as `pyttsx3`, `smtplib`, `requests`, and `BeautifulSoup`.

2. **Running the Script**:
   - Run the script, and it will fetch the latest Friday sermon summary, convert it to audio, upload it to Google Drive, and send an email with the shareable link.

3. **Customization**:
   - You can customize the script by modifying the URL of the sermon summary page, date, and other settings as needed.

## Security Note

Make sure to keep your API keys and credentials secure and do not share them publicly. Use environment variables or a configuration file to store sensitive information.

## Credits

This script was created to simplify the process of staying updated with Friday sermons. It uses various open-source libraries and APIs.

Feel free to modify and use this script according to your requirements.

Happy listening!
