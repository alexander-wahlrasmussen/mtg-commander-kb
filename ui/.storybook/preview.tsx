import React from "react";
import type { Preview } from "@storybook/react";
import "../src/theme/tokens.css";

// Wrap every story in the dark token surface so previews look like the app
// (and so /design-sync bundles this as the preview wrapper).
const preview: Preview = {
  parameters: {
    layout: "fullscreen",
    backgrounds: { disable: true },
  },
  decorators: [
    (Story) =>
      React.createElement(
        "div",
        { style: { background: "var(--bg)", color: "var(--text)", padding: 24, minHeight: "100vh", fontFamily: "var(--font)" } },
        React.createElement(Story),
      ),
  ],
};

export default preview;
