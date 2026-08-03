export default function PuzzleInfo({ category, reason }) {
  return (
    <div
      style={{
        marginTop: "20px",
        fontSize: "18px",
      }}
    >
      <h3>Puzzle Type: {category}</h3>
      <p>Lesson: {reason}</p>
    </div>
  );
}