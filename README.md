# Air-Justice-Lab
This is a working repository for the Dash Application I am building for the Air Justice Lab at the Media Sanctuary in Troy, NY.
The Air Justice Lab owns purple air sensors in various locations across the Capital Region that track temperature, pressure, humidity, and particulate matter.

I have completed a proof of concept that displays data from the purple air sensors owned by the Air Justice Lab broken down into 3 pages:

Page 1: AQI intensity by hour at each sensor location
- Intensity is determined by dividing the recorded average AQI for that hour by 300 (the highest binned AQI severity level). The closer an intensity is to 1, the more unhealthy its level is.
![52105D41-1D11-4E04-9D47-31FE434A5426](https://github.com/user-attachments/assets/1d70ca77-6015-4da6-9a83-e768fa919d97)

Page 2: Annual Bad AQI
- The total number of bad AQI readings (AQI > 100) are totaled for each sensor by year.
- Year was chosen because there tends to be very few bad AQI readings given that the data is collected in 10 minute intervals
![717D6260-00DE-41ED-BAFC-B783D64B358A](https://github.com/user-attachments/assets/57ed0584-bc99-4c70-85b5-0768109ff842)

Page 3: Monthly AQI
- The AQI readings for each sensor are totaled by month and categorically binned into each AQI severity level
- The average AQI per hour is also broken out to give an idea of how the AQI fluctuates by sensor through out the day for that month
![5F6DF3A1-4CB7-4F6A-A9EC-7B4CBB61BC25](https://github.com/user-attachments/assets/baf759a6-ed08-491e-bd60-75ac278c2aca)

There are definitely other ways to view this data.
As of right now this is a proof of concept that is subject to change when given feedback.
