export async function getEmails() {
  const response = await fetch('/api');
  const json = await response.json();
  return json.items;
}

export async function updateEmail(id, data) {
  const response = await fetch(`/api/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });
  return await response.json();
}
