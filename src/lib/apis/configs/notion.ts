import { WEBUI_API_BASE_URL } from '$lib/constants';

/** Notion Integration Config **/
export const getNotionConfig = async (token: string) => {
  let error = null;
  const res = await fetch(`${WEBUI_API_BASE_URL}/configs/notion`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.error(err);
      error = err.detail;
      return null;
    });
  if (error) throw error;
  return res;
};

export const updateNotionConfig = async (
  token: string,
  config: { NOTION_CLIENT_ID: string; NOTION_CLIENT_SECRET: string; NOTION_REDIRECT_URI: string }
) => {
  let error = null;
  const res = await fetch(`${WEBUI_API_BASE_URL}/configs/notion`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ ...config }),
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.error(err);
      error = err.detail;
      return null;
    });
  if (error) throw error;
  return res;
};