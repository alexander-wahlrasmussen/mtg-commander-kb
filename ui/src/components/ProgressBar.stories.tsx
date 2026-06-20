import type { Meta, StoryObj } from "@storybook/react";
import { ProgressBar } from "./ProgressBar";

const meta: Meta<typeof ProgressBar> = { title: "ProgressBar", component: ProgressBar };
export default meta;
type Story = StoryObj<typeof ProgressBar>;

// Pinned to the top of the viewport; shows the indeterminate sliding accent bar.
export const Active: Story = { args: { active: true } };
export const Idle: Story = { args: { active: false } };
