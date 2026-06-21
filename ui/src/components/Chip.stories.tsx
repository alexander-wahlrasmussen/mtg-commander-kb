import type { Meta, StoryObj } from "@storybook/react";
import { Chip } from "./Chip";

const meta: Meta<typeof Chip> = { title: "Chip", component: Chip };
export default meta;
type Story = StoryObj<typeof Chip>;

export const Off: Story = { args: { label: "Lightning War", color: "#fe8019" } };
export const On: Story = { args: { label: "Radiation Sickness", active: true, color: "#b8bb26" } };

export const Row: Story = {
  render: () => (
    <div style={{ display: "flex", gap: 7, flexWrap: "wrap" }}>
      <Chip label="Genome Project" active color="#fe8019" />
      <Chip label="Radiation Sickness" active color="#fabd2f" />
      <Chip label="Grand Design" color="#b8bb26" />
      <Chip label="Calamity Tax" color="#d3869b" />
    </div>
  ),
};
