# HiveSight

HiveSight is a powerful tool that allows you to ask questions to a large number of Language Models (LLMs) that can simulate various human perspectives. With HiveSight, you can gain insights into how different individuals or groups might respond to a given question based on their beliefs, values, and decision-making processes.

The tool is deployed at [hivesight.ai](https://hivesight.ai), making it easily accessible to users.

## Features

- Ask binary (yes/no) questions to LLMs
- Specify the number of queries to run
- Choose between custom perspectives or random perspectives from a dataset
- Request explanations for the responses
- Adjust temperature and top_p values for generating responses
- View the percentage of 'yes' responses along with a 95% confidence interval
- Download the raw responses as a CSV file
- Store run information and responses in a Google Spreadsheet

## Examples

### Example 1: Custom Perspective

1. Go to [hivesight.ai](https://hivesight.ai)
2. Enter your binary question: "Should we invest more in renewable energy?"
3. Select the number of queries: 20
4. Choose "Custom" perspective type
5. Enter the role or persona: "Environmental activist"
6. Click "Run LLM Multiple Times"

HiveSight will generate responses from the perspective of an environmental activist, providing insights into how they might approach the question of investing in renewable energy.

### Example 2: Random Perspective from Dataset

1. Go to [hivesight.ai](https://hivesight.ai)
2. Enter your binary question: "Is it important to save for retirement early?"
3. Select the number of queries: 15
4. Choose "Random from Dataset" perspective type
5. Enable "Request Explanation"
6. Click "Run LLM Multiple Times"

HiveSight will select a random perspective from PolicyEngine's calibrated nationwide survey dataset, such as "35-year-old from California with annual income of $75,000," and generate responses based on that perspective. The tool will provide the percentage of 'yes' responses, a confidence interval, and a summary of the explanations given by the LLMs.

## Requirements

- Web browser to access [hivesight.ai](https://hivesight.ai)

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Dataset provided by [PolicyEngine](https://policyengine.org), originating from the Current Population Survey and enhanced with tax records and calibrated to match national demographic and economic aggregate characteristics
- Built using Streamlit, Pandas, Google Sheets API, OpenAI API, and Anthropic API
