import type { Meta, StoryObj } from "@storybook/react";
import { SegmentedControl } from "./SegmentedControl";

const meta: Meta<typeof SegmentedControl> = { title: "SegmentedControl", component: SegmentedControl };
export default meta;
type Story = StoryObj<typeof SegmentedControl>;

export const PodSpeed: Story = {
  args: {
    options: [
      { value: "fast", label: "fast" },
      { value: "base", label: "base" },
      { value: "slow", label: "slow" },
    ],
    value: "base",
    onChange: () => {},
  },
};

export const TwoOptions: Story = {
  args: {
    options: [
      { value: "decap", label: "decap" },
      { value: "table", label: "table" },
    ],
    value: "decap",
    onChange: () => {},
  },
};
