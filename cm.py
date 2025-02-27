import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://cf.090227.xyz/index.html"

# Send a GET request to the URL to fetch the webpage content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table in the HTML
    table = soup.find('table')
    
    # Open a file in write mode to save the IP addresses
    with open("valid_ips.txt", "w") as file:
        count = 1  # Initialize counter for numbering IPs
        
        # Loop through all the rows in the table (except the header)
        for row in table.find_all('tr')[1:]:
            # Find all the cells in the current row
            cells = row.find_all('td')
            
            # Check if the row has enough columns
            if len(cells) > 4:
                # Extract the IP address and speed
                ip = cells[1].text.strip()
                speed = cells[4].text.strip()
                
                # If speed is not "0.00MB/s", write the IP to the file
              #  if speed != "0.00MB/s":
                if speed = "0.00MB/s":
                    file.write(f"{ip}#CM大佬{count}\n")
                    count += 1  # Increment the counter
    
    print("Valid IPs have been written to 'valid_ips.txt'.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
