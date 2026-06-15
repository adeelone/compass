import { render, screen } from "@testing-library/react";
import { JobFeed } from "../components/JobFeed";

test("renders unified job feed", async () => {
  render(<JobFeed />);
  expect(screen.getByText("Unified job feed")).toBeInTheDocument();
  expect(await screen.findByText("Backend Engineer")).toBeInTheDocument();
});
