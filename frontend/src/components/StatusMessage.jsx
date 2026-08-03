export default function StatusMessage({ message }) {
  if (!message) return null;

  return (
    <div style={{
      marginTop: "20px",
      fontSize: "20px",
      textAlign: "center"
    }}>
      {message}
    </div>
  );
}