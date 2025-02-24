import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      // GitHub: "https://github.com/jackyzha0/quartz",
      "GitHub": "https://github.com/shihaocao",
      // "Discord Community": "https://discord.gg/cRFFHYye7t",
      "LinkedIn": "https://www.linkedin.com/in/shihaocao/",
      "Twitter": "https://x.com/shihao_cao",
      "Resume": "https://www.shihaocao.com/assets/Shihao_Cao_Resume.pdf",
      "Instagram": "https://www.instagram.com/shihaocao88/",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    // Component.Darkmode(),
    Component.Explorer(),
  ],
  right: [
    Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    // Component.Darkmode(),
    Component.Explorer(),
  ],
  right: [],
}
