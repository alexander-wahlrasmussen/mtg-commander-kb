import type { Meta, StoryObj } from "@storybook/react";
import { Card } from "./Card";

const meta: Meta<typeof Card> = { title: "Card", component: Card };
export default meta;
type Story = StoryObj<typeof Card>;

export const Default: Story = {
  args: {
    title: "P(beat the T6-7 pod)",
    hint: "· DECAP clock",
    children: <p style={{ margin: 0, color: "var(--muted)" }}>Card body content goes here.</p>,
  },
};

export const NoHeading: Story = {
  args: { children: <p style={{ margin: 0 }}>A chrome-less panel with no title.</p> },
};
