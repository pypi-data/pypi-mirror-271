local dap = require("dap")

dap.adapters.python = {
	type = "server",
	host = "127.0.0.1",
	port = 5678,
}

dap.configurations.python = {
	{
		name = "Python: Remote Attach",
		type = "python",
		request = "attach",
		connect = {
			host = "127.0.0.1",
			port = 5678,
		},
		-- pathMappings = {
		-- 	{
		-- 		localRoot = function()
		-- 			return vim.fn.input("Local code folder > ", vim.fn.getcwd(), "file")
		-- 		end,
		-- 		remoteRoot = function()
		-- 			return vim.fn.input("Container code folder > ", "/", "file")
		-- 		end,
		-- 	},
		-- },
		-- justMyCode = true,
	},
}
