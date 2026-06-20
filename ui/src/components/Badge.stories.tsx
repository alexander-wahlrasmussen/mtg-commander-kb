import type { Meta, StoryObj } from "@storybook/react";
import { Badge } from "./Badge";

const meta: Meta<typeof Badge> = { title: "Badge", component: Badge };
export default meta;
type Story = StoryObj<typeof Badge>;

export const Ready: Story = { args: { children: "ready" } };
export const Busy: Story = { args: { children: "running…", variant: "busy" } };
export const Ok: Story = { args: { children: "16 decks · 12k trials", variant: "ok" } };
export const Error: Story = { args: { children: "error: timeout", variant: "err" } };

export const AllVariants: Story = {
  render: () => (
    <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
      <Badge>ready</Badge>
      <Badge variant="busy">running…</Badge>
      <Badge variant="ok">done</Badge>
      <Badge variant="err">error</Badge>
    </div>
  ),
};
