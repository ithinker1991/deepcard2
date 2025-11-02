export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-gray-900 dark:text-white mb-4">
            DeepCard
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            AI-Powered Flashcard Application
          </p>
          <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            🚀 Currently in Development
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-4xl mx-auto">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <div className="text-3xl mb-4">🤖</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              AI Generation
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              Generate flashcards from any content using multiple LLM providers
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <div className="text-3xl mb-4">🌐</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              URL Support
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              Extract content from articles, blogs, and webpages automatically
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <div className="text-3xl mb-4">🧠</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Smart Learning
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              Spaced repetition algorithms for optimal memory retention
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Fast & Simple
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              Clean interface focused on core functionality
            </p>
          </div>
        </div>

        <div className="mt-16 text-center">
          <div className="inline-flex flex-col items-center p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Development Progress
            </h2>
            <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-300">
              <span>📋</span>
              <span>Roadmap defined, starting Milestone 1</span>
            </div>
            <div className="mt-4 text-xs text-gray-500 dark:text-gray-400">
              Check <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">ROADMAP.md</code> for details
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}