
<h1 align="center"> Darwin 🤖 - AI Software Engineer Intern</h1>


> [!IMPORTANT]  
> At its early developmental stage, this project is still experimental and lacks many implemented features. Contributions are encouraged to advance its progress.

## Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [Roadmap for Development](#roadmap-for-development)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)🤖
  - [How to use](#how-to-use)
- [Help and Support](#help-and-support)
- [License](#license)

## About

Darwin is the first in the series of multiple AI Engineers with the capability to comprehend complex human commands, dissect them into actionable steps, conduct research, and generate code to accomplish the specified task all powered by LLMs.

The idea behind Darwin is to create an AI SWE Intern to assist in basic tasks. Whether you require assistance in creating a new feature, resolving a bug, or building an entire project from the ground up, Darwin is ready to support you every step of the way.

> [!NOTE]
> Darwin is being developed after the influence from [Devin](https://www.cognition-labs.com/introducing-devin) and [Devika](https://github.com/stitionai/devika). Starting as an alternative to an intern, we aim to eventually reach the competency of an ML/AI Engineer.

## Key Features

- 🧠 Capable of comprehending complex codebases and architectures
- 🔧 Skillful in managing changes, updates, and bug fixes within software projects
- 📚 Conducts thorough research to gather pertinent information
- 💡 Engages in brainstorming sessions to generate innovative ideas
- 💻 Writes code in multiple programming languages proficiently

## Roadmap for Development

- **Solving GitHub Issues**: Enhance the ability to track, manage, and resolve GitHub issues efficiently within the software.
  
- **Building Model Pipelines**: Develop a feature to create and optimize model pipelines for improved performance and productivity.

- **Training Models**: Implement functionality for training models with diverse datasets to enhance accuracy and performance.


## Getting Started

### Requirements
```
Version's requirements
  - Python >= 3.9 and < 3.12
  - NodeJs >= 18
```

### Installation

To install npm

#### For Mac
```
# installs NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# download and install Node.js
nvm install 20
# verifies the right Node.js version is in the environment
node -v # should print `v20.12.2`
# verifies the right NPM version is in the environment
npm -v # should print `10.5.0`
```

#### For Windows
```
# download and install Node.js
choco install nodejs-lts --version="20.12.2"
# verifies the right Node.js version is in the environment
node -v # should print `v20.12.2`
# verifies the right NPM version is in the environment
npm -v # should print `10.5.0`
```

To install Darwin, follow these steps:

1. Clone the Darwin repository:
```
git clone https://github.com/Cognation/darwin.git
```
2. Navigate to the project directory:
```
cd darwin
```
3. Create a virtual environment/conda environment and install the required dependencies (you can use any virtual environment manager):
```
conda create -n darwin python=3.11
conda activate darwin
```

4. Install the dependencies
Installing python packages:
```
pip install -r requirements.txt
```

5. Setup the frontend
```
cd ui
npm install
```

### How to use
Now you just need to add your OpenAI key to a .env file, you can use this command:
```
echo "OPENAI_API_KEY='<your_OpenAI_key>' " > .env
export OPENAI_API_KEY=<your_OpenAI_key>
```
If you are a windows user, set your OpenAI key using
```bash
setx OPENAI_API_KEY "your-api-key-here"
```
All your data is stored on your machine, initialise your database using:
```
mkdir ./data && touch ./data/data.db && echo '{}' > ./data/data.db
```
## Spinning up Darwin
You can start using Darwin with these two lines of command
### Starting the server
```
python3 server.py
```
### Initialising the UI
```
cd ui
npm start
```

## Help and Support

Should you have any queries, feedback, or ideas, do not hesitate to contact us. You can submit an issue through the [issue tracker](https://github.com/_/_/issues) or participate in our [discussions](https://github.com/_/_/discussions) for overall conversations.

Furthermore, we also host a Discord server for the Darwin community, providing a platform for users to interact, exchange experiences, seek assistance, and engage in project collaboration. To join the Darwin community Discord server, simply [click here](https://discord.gg/dY8E6KUd).

## License

Darwin is released under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for more information.

---

We hope you find Darwin to be a valuable tool in your software development journey. If you have any questions, feedback, or suggestions, please don't hesitate to reach out. Happy coding with Darwin!