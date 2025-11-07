# Zara
Nothing special just a mass proxy checker at high-speed, asynchronous proxy checker written in Python. It allows you to mass-check HTTP proxies for availability, providing real-time statistics and saving working proxies to a file.

## Features

- **Fast & Concurrent**: Designed to handle thousands of proxies concurrently using asyncio and aiohttp.
- **Live Progress Reporting**: Displays checked count, live speed, percentage progress, and the number of working proxies found.
- **Easy to Use**: Just put proxies in a text file and run.

## Usage

1. **Install Requirements**  
   Install dependencies using pip:
   ```
   pip install aiohttp
   ```

2. **Prepare Proxies**  
   Format:  
   ```
   host:port
   ```
   Save your proxy list as `proxies.txt` or specify another filename when running.

3. **Run the Checker**  
   ```
   python Checker.py [proxies.txt]
   ```
   The program will use `proxies.txt` by default.

4. **Results**  
   Working proxies are saved to `working.txt` after the check completes.

## Customization

- You can change concurrency, timeout, or test URL at the top of `Checker.py`.
- Supports HTTP proxies only by default.

## Credit

Created by Reinhart  
Zara v1.0

## License

[MIT License](LICENSE)
