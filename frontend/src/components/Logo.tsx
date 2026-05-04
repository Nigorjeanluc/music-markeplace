export default function Logo() {
  return (
    <span className="font-black tracking-tight text-lg leading-none select-none">
      <span style={{
        background: 'linear-gradient(135deg, #00e5ff 0%, #00b8cc 50%, #aa3bff 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        filter: 'drop-shadow(0 0 8px #00e5ff66)',
      }}>
        Music
      </span>
      <span className="text-white font-light tracking-widest text-sm ml-1 uppercase">
        Marketplace
      </span>
    </span>
  )
}
