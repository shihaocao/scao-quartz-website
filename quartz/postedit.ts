import * as fs from 'fs';
import * as path from 'path';

// Define the target directory
const TARGET_DIR = 'public';

// Define the replacement patterns
const replacements: [RegExp, string][] = [
    [/href="\."/g, 'href="core.html"'],
    [/href="\.\//g, 'href="core.html"']
];

function replaceInFile(filePath: string) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        
        let updatedContent = content.split('\n').map(line => {
            return line.replace('href="."', 'href="core.html"').replace('href="./"', 'href="core.html"').replace('href="/"', 'href="core.html"');
        }).join('\n');

        fs.writeFileSync(filePath, updatedContent, 'utf8');
        console.log(`Updated: ${filePath}`);
    } catch (error) {
        console.error(`Error processing ${filePath}:`, error);
    }
}


export function processDirectory(directory: string) {
    fs.readdirSync(directory).forEach(file => {
        const fullPath = path.join(directory, file);
        if (fs.statSync(fullPath).isDirectory()) {
            processDirectory(fullPath);
        } else {
            replaceInFile(fullPath);
        }
    });
}