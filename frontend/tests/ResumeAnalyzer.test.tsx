import { render, screen } from "@testing-library/react";
import { ResumeAnalyzer } from "../components/ResumeAnalyzer";

test("renders resume analyzer", () => {
  render(<ResumeAnalyzer />);
  expect(screen.getByText("Resume intelligence")).toBeInTheDocument();
});

