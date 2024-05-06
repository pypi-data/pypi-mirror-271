<h1>easy_code_to_text Project</h1>
<p>A Python package to concatenate code files into a single document, with support for multiple programming languages and customizable ignore patterns.</p>

<h2>Features</h2>
<ul>
    <li>Support for multiple programming languages including Python, JavaScript, HTML, CSS, Java, and YAML.</li>
    <li>Customizable ignore patterns to exclude specific files or directories.</li>
    <li>Generates a single document with clear demarcation for each file's path and language.</li>
</ul>

<h2>Installation</h2>
<p>The package can be installed via pip:</p>
<pre><code>pip install code_to_text</code></pre>

<h2>Usage</h2>
<p>After installation, you can use the package as follows:</p>
<pre><code>from code_to_text import read_and_combine_files

read_and_combine_files(input_directory='your_code_directory',
                       output_file='your_output_file.txt',
                       ignore_file_path='your_ignore_file.txt')</code></pre>

<h2>Configuration</h2>
<h3>Ignore File</h3>
<p>Create an ignore file (e.g., <code>.codeToTextIgnore</code>) in your project root with patterns to ignore:</p>
<pre><code>*.log
node_modules/
build/</code></pre>

<h2>Contributing</h2>
<p>We welcome contributions! Please follow these steps to contribute:</p>
<ol>
    <li>Fork the repository.</li>
    <li>Create a new branch for each feature or improvement.</li>
    <li>Submit a pull request with a comprehensive description of changes.</li>
</ol>

<h2>License</h2>
<p>This project is open source and available under the MIT License. Benjamin QUINET.</p>
