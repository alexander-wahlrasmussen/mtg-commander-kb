import type { Meta, StoryObj } from "@storybook/react";
import { Slider } from "./Slider";

const meta: Meta<typeof Slider> = { title: "Slider", component: Slider };
export default meta;
type Story = StoryObj<typeof Slider>;

export const AbolisherProbability: Story = {
  args: { label: "Abolisher P(out)", value: 0.3, min: 0, max: 1, step: 0.05, display: "0.30", onChange: () => {} },
};

export const Trials: Story = {
  args: { label: "Trials", value: 12000, min: 2000, max: 60000, step: 2000, display: "12k", onChange: () => {} },
};

export const Frozen: Story = {
  args: { label: "Trials", value: 20000, min: 2000, max: 60000, step: 2000, display: "20k (baked)", frozen: true },
};
