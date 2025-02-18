import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const Header: QuartzComponent = ({ cfg, tree, children, fileData }: QuartzComponentProps) => {
  // console.log("FOO")
  // console.log(tree)
  // console.log(fileData)
  // const title = cfg?.pageTitle;
  // if (title !== "Shihao's Site") {
  // Terrible Terrible Hack to see if we're on the main landing page LOL
  return null;
  if (fileData.filePath !== "content/index.md") {
    return null;
  }
  return (
    <div className="header-container">
      <div className="spacer"></div> {/* Left Spacer */}
      <div className="customheaderdiv">
        <br />
        <h1>Hello! I'm Shihao</h1>
        <p>Welcome</p>
        <p>Things I am grateful for</p>
        <ul>
          <li>The opportunity to be alive</li>
          <li>The opportunity to grow</li>
          <li>Longboarding</li>
        </ul>
      </div>
      <div className="spacer"></div> {/* Right Spacer */}
      <div className="spacer"></div> {/* Right Spacer */}

    </div>
  );
};


Header.css = `
.header-container {
  display: flex;
  width: 100%; /* Full width of the page */
}

.spacer {
  flex-grow: 1; /* Spacers expand to fill available space */
}

.customheaderdiv {
  width: 20em;
  text-align: left; /* Ensures content remains left-aligned */
}


header {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 2rem 0;
  gap: 1.5rem;
}

header h1 {
  margin: 0;
  flex: auto;
}
`

export default (() => Header) satisfies QuartzComponentConstructor
