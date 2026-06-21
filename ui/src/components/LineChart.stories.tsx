import type { Meta, StoryObj } from "@storybook/react";
import { LineChart } from "./LineChart";

const meta: Meta<typeof LineChart> = { title: "Charts/LineChart", component: LineChart };
export default meta;
type Story = StoryObj<typeof LineChart>;

const curve = (slug: number) =>
  [4, 5, 6, 7, 8, 9, 10, 12].map((t) => ({ x: t, y: Math.round(100 / (1 + Math.exp(-(t - (6 + slug))))) }));

export const ClockCurves: Story = {
  args: {
    height: 380,
    xLabel: "turn",
    yLabel: "cum P(decap ≤ turn) %",
    refLineY: 50,
    series: [
      { name: "Radiation Sickness", color: "#fe8019", points: curve(0) },
      { name: "The Genome Project", color: "#fabd2f", points: curve(1) },
      { name: "The Replication Crisis", color: "#b8bb26", points: curve(2) },
      { name: "The Grand Design", color: "#fb4934", points: curve(4) },
    ],
  },
};
