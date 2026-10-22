
import streamlit as st
from urllib.parse import quote, unquote, urlencode, parse_qsl, urlsplit

st.set_page_config(
    page_title="URL Toolkit",
    page_icon="🔗",
    layout="centered"
)

st.title("🔗 URL Encoder & Decoder")
st.caption("A simple developer tool to encode URLs, decode URLs, and work with query parameters.")

st.divider()

mode = st.radio(
    "Choose a tool",
    [
        "URL Encoder",
        "URL Decoder",
        "Query Parameter Encoder",
        "Query Parameter Decoder"
    ],
    horizontal=False
)

if mode == "URL Encoder":
    st.subheader("Encode a URL or text")
    st.caption("Converts special characters into percent-encoded form.")

    text = st.text_area(
        "Enter URL or text",
        placeholder="Example: https://example.com/search?q=hello world",
        height=130,
        key="encode_input"
    )

    safe_url = st.checkbox(
        "Preserve URL structure (/, :, ?, &, =)",
        value=True
    )

    if st.button("Encode", type="primary", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text to encode.")
        else:
            result = quote(
                text,
                safe=":/?&=#%+-._~" if safe_url else ""
            )
            st.session_state["result"] = result

elif mode == "URL Decoder":
    st.subheader("Decode an encoded URL or text")
    st.caption("Converts percent-encoded characters back to readable text.")

    text = st.text_area(
        "Enter encoded URL or text",
        placeholder="Example: hello%20world",
        height=130,
        key="decode_input"
    )

    if st.button("Decode", type="primary", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text to decode.")
        else:
            try:
                result = unquote(text, encoding="utf-8", errors="strict")
                st.session_state["result"] = result
            except (UnicodeDecodeError, ValueError):
                st.error("The input could not be decoded as valid UTF-8.")

elif mode == "Query Parameter Encoder":
    st.subheader("Encode query parameters")
    st.caption("Enter key-value pairs to generate a URL query string.")

    pairs_text = st.text_area(
        "Enter one key=value pair per line",
        placeholder="name=Shrinivas\ncity=Bhatkal\ncourse=Computer Science",
        height=130,
        key="pairs_encode"
    )

    if st.button("Encode Parameters", type="primary", use_container_width=True):
        if not pairs_text.strip():
            st.warning("Please enter at least one key=value pair.")
        else:
            pairs = []
            valid = True

            for line in pairs_text.splitlines():
                if not line.strip():
                    continue

                if "=" not in line:
                    st.error(f"Invalid line: {line}. Use key=value format.")
                    valid = False
                    break

                key, value = line.split("=", 1)
                pairs.append((key.strip(), value.strip()))

            if valid and pairs:
                st.session_state["result"] = urlencode(pairs)
            elif valid:
                st.warning("Please enter at least one valid pair.")

elif mode == "Query Parameter Decoder":
    st.subheader("Decode query parameters")
    st.caption("Paste a query string to view its keys and values.")

    query = st.text_input(
        "Enter query string",
        placeholder="name=Shrinivas&city=Bhatkal",
        key="query_decode"
    )

    if st.button("Decode Parameters", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a query string.")
        else:
            try:
                parts = urlsplit(query)
                query_string = parts.query if "?" in query else query
                params = parse_qsl(
                    query_string,
                    keep_blank_values=True,
                    strict_parsing=True,
                    encoding="utf-8",
                    errors="strict"
                )

                if not params:
                    st.warning("No query parameters found.")
                else:
                    st.session_state["result"] = "\n".join(
                        f"{key} = {value}" for key, value in params
                    )
            except (ValueError, UnicodeDecodeError):
                st.error("Invalid query parameters. Please check the input.")

if "result" in st.session_state:
    st.divider()
    st.subheader("Result")

    st.text_area(
        "Output",
        value=st.session_state["result"],
        height=130,
        key="output_display"
    )

    st.download_button(
        "⬇️ Download Result",
        data=st.session_state["result"],
        file_name="url_result.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.caption("Select and copy the result above. The download button saves it as a text file.")

st.divider()

with st.expander("💡 Try these examples"):
    st.markdown(
        """
        **URL encoding**

        Input: `hello world & Python`

        Output: `hello%20world%20%26%20Python`

        **URL decoding**

        Input: `hello%20world`

        Output: `hello world`

        **Query parameters**

        Input:
        ```
        name=Shrinivas
        city=Bhatkal
        ```

        Output: `name=Shrinivas&city=Bhatkal`
        """
    )

st.caption("Built with Python, Streamlit and urllib.parse.")
