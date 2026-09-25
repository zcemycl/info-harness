import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";

const components: Components = {
  table({ children }) {
    return (
      <div className="my-2 overflow-x-auto">
        <table>{children}</table>
      </div>
    );
  },
};

export function MarkdownMessage({ text }: { text: string }) {
  return (
    <div className="markdown">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw, rehypeSanitize]} components={components}>
        {text}
      </ReactMarkdown>
    </div>
  );
}
