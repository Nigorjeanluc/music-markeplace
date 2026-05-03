import { render, screen } from '@testing-library/react'
import Logo from './Logo'

describe('Logo', () => {
  it('renders the brand text', () => {
    render(<Logo />)

    expect(screen.getByText('Music')).toBeInTheDocument()
    expect(screen.getByText('Marketplace')).toBeInTheDocument()
  })
})
