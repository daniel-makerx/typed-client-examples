import { Command } from 'commander'
import { load } from './schema/load'
import * as path from 'path'
import { generate } from './client/generate'
import { writeDocumentPartsToStream } from './output/writer'
import fs from 'fs'
import { boom } from './util/boom'

export function cli(workingDirectory: string, args: string[]) {
  const program = new Command()
  program
    .command('generate')
    .description('Generates a TypeScript client for the given application.json file')
    .option('-a --application <path>', 'Specifies the application.json file')
    .option('-o --output <path>', 'Specifies the output file path')
    .action(({ application, output }: { application?: string; output?: string }): void => {
      if (!application) return boom('Please specify a path to the application spec')
      if (!output) return boom('Please specify an output path for the client')
      const spec = load(path.resolve(workingDirectory, application))

      const parts = generate(spec)

      const file = fs.createWriteStream(path.resolve(workingDirectory, output), {
        flags: 'w',
      })
      writeDocumentPartsToStream(parts, file)
    })

  program.parse(args)
}
