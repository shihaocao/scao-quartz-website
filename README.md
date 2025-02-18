# Quartz v4

## SCAO
```
nvm use node
npx quartz build --serve
```

> “[One] who works with the door open gets all kinds of interruptions, but [they] also occasionally gets clues as to what the world is and what might be important.” — Richard Hamming

Quartz is a set of tools that helps you publish your [digital garden](https://jzhao.xyz/posts/networked-thought) and notes as a website for free.
Quartz v4 features a from-the-ground rewrite focusing on end-user extensibility and ease-of-use.

🔗 Read the documentation and get started: https://quartz.jzhao.xyz/

[Join the Discord Community](https://discord.gg/cRFFHYye7t)

## Sponsors

<p align="center">
  <a href="https://github.com/sponsors/jackyzha0">
    <img src="https://cdn.jsdelivr.net/gh/jackyzha0/jackyzha0/sponsorkit/sponsors.svg" />
  </a>
</p>


## 02/04

I did two terrible things

```

const Header: QuartzComponent = ({ cfg, tree, children, fileData }: QuartzComponentProps) => {
  // console.log("FOO")
  // console.log(tree)
  // console.log(fileData)
  // const title = cfg?.pageTitle;
  // if (title !== "Shihao's Site") {
  // Terrible Terrible Hack to see if we're on the main landing page LOL
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
```

Wrote this garbage to make a custom header. This seems... wrong but whatever lol

Secondly, I can't figure out how to turn off darkmode. So I went to `quartz.layout.ts` and commented out `Darkmode()`