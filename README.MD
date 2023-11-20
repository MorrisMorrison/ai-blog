# ai-blog
This Python script leverages ChatGPT to generate blog posts and publishes them to Hashnode.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MorrisMorrison/ai-blog.git
   cd ai-blog
   ```
2. Install the required dependencies:
   `pip install -r requirements.txt`
   
## Configuration
Before running the script, make sure to set the following environment variables:
   - **CHATGPT_API_KEY**: Your ChatGPT API key.
   - **HASNODE_API_KEY**: Your Hashnode API key.
   - **HASNODE_PUBLICATION_ID**: The Hashnode publication ID - can be retrieved via Hashnode API or from the URL of the publication/blog dashboard.

You can set your prompt in `generate-content-prompt.txt`

## Usage
Run the script with:

- `python3 main.py`
- `python3 main.py --scheduled` - schedules the script.
  Scheduling can currently only be configured by manipulating the code

This will prompt the script to generate a blog post using ChatGPT and publish it to Hashnode.

## Contributing
If you'd like to contribute to this project, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix: git checkout -b feature/my-feature.
- Make your changes and commit them: git commit -m 'Add some feature'.
- Push to the branch: git push origin feature/my-feature.
- Submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
