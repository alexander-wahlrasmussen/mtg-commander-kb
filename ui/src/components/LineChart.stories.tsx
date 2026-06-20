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
      { name: "Radiation Sickness", color: "#5cd2ff", points: curve(0) },
      { name: "The Genome Project", color: "#ffb454", points: curve(1) },
      { name: "The Replication Crisis", color: "#46d39a", points: curve(2) },
      { name: "The Grand Design", color: "#ff6b6b", points: curve(4) },
    ],
  },
};
