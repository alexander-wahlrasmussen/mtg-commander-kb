import type { Meta, StoryObj } from "@storybook/react";
import { Chip } from "./Chip";

const meta: Meta<typeof Chip> = { title: "Chip", component: Chip };
export default meta;
type Story = StoryObj<typeof Chip>;

export const Off: Story = { args: { label: "Lightning War", color: "#5cd2ff" } };
export const On: Story = { args: { label: "Radiation Sickness", active: true, color: "#46d39a" } };

export const Row: Story = {
  render: () => (
    <div style={{ display: "flex", gap: 7, flexWrap: "wrap" }}>
      <Chip label="Genome Project" active color="#5cd2ff" />
      <Chip label="Radiation Sickness" active color="#ffb454" />
      <Chip label="Grand Design" color="#46d39a" />
      <Chip label="Calamity Tax" color="#b48cff" />
    </div>
  ),
};
